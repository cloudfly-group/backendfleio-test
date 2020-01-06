import logging
import datetime

from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import Q
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _

from rest_framework import filters, mixins, viewsets
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter
from fleio.core.exceptions import APIBadRequest
from fleio.core.models import AppUser, Client

from fleio.utils.collections import get_new_or_none

from plugins.tickets.common.ticket_notification_dispatcher import ticket_notifications_dispatcher
from plugins.tickets.common.tickets_utils import TicketUtils
from plugins.tickets.common.attachments_storage import AttachmentsStorage
from plugins.tickets.common.tickets_filters import TicketIdSearchFilter

from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket_update import TicketUpdate
from plugins.tickets.models import TicketNote
from plugins.tickets.models.ticket import TicketPriority
from plugins.tickets.models.ticket import TicketStatus
from plugins.tickets.models.ticket import TicketLink
from plugins.tickets.models.attachment import Attachment
from plugins.tickets.models.signature import StaffSignature


from plugins.tickets.staff.tickets.serializers import TicketBriefSerializer, TicketSerializer
from plugins.tickets.staff.tickets.serializers import TicketUpdateUpdateSerializer
from plugins.tickets.staff.tickets.serializers import TicketListSerializer
from plugins.tickets.staff.tickets.serializers import TicketNoteSerializer
from plugins.tickets.staff.tickets.serializers import TicketLinkSerializer


LOG = logging.getLogger(__name__)


class TicketLinkViewSet(viewsets.ModelViewSet):
    serializer_class = TicketLinkSerializer
    permission_classes = (StaffOnly,)
    queryset = TicketLink.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = (
        'ticket',
        'linked_ticket',
    )
    ordering_fields = ('id', 'ticket', 'linked_ticket',)
    filter_fields = ('ticket', 'linked_ticket',)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        symmetrical = serializer.validated_data.get('symmetrical', False)
        if 'symmetrical' in serializer.validated_data:
            del serializer.validated_data['symmetrical']
        ticket = serializer.validated_data.get('ticket')
        linked_ticket = serializer.validated_data.get('linked_ticket')
        if ticket == linked_ticket:
            raise ValidationError(_('Cannot link ticket to itself.'))
        serializer.save()
        if symmetrical is True:
            # creates the symmetrical relation
            with transaction.atomic():
                try:
                    TicketLink.objects.create(ticket=linked_ticket, linked_ticket=ticket)
                except IntegrityError:
                    pass

    def destroy(self, request, *args, **kwargs):
        return Response(status=501, data={'detail': _('Not implemented')})

    @action(detail=True, methods=['post'])
    def delete_link(self, request, pk):
        del pk  # unused
        instance = self.get_object()
        delete_symmetrical = request.data.get('delete_symmetrical', False)
        msg = _('Link deleted')
        with transaction.atomic():
            if delete_symmetrical is True:
                try:
                    symmetrical_link = TicketLink.objects.get(
                        ticket=instance.linked_ticket,
                        linked_ticket=instance.ticket
                    )
                    msg = _('Links deleted')
                    symmetrical_link.delete()
                except TicketLink.DoesNotExist:
                    pass
            instance.delete()
            return Response(
                status=200,
                data={'details': msg}
            )


class TicketNotesViewSet(mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    serializer_class = TicketNoteSerializer
    permission_classes = (StaffOnly,)
    queryset = TicketNote.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        now = datetime.datetime.now()
        serializer.save(last_edited_by=user, last_edited=now)

    def perform_destroy(self, instance):
        attachment_storage = AttachmentsStorage.get_attachments_storage()
        for attachment in instance.attachments.all():
            attachment_storage.remove_attachment_from_disk(disk_file=attachment.disk_file)
        instance.delete()


class TicketUpdateViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = TicketUpdateUpdateSerializer
    queryset = TicketUpdate.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        now = datetime.datetime.now()
        serializer.save(last_edited_by=user, last_edited=now)

    def perform_destroy(self, instance):
        attachment_storage = AttachmentsStorage.get_attachments_storage()
        for attachment in instance.attachments.all():
            attachment_storage.remove_attachment_from_disk(disk_file=attachment.disk_file)
        instance.delete()


class TicketsViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter,
                       TicketIdSearchFilter)
    search_fields = (
        'id',
        'assigned_to__first_name',
        'assigned_to__last_name',
        'created_by__first_name',
        'created_by__last_name',
        'description',
        'status',
        'title',
    )
    ordering_fields = ('assigned_to', 'created_at', 'last_reply_at', 'created_by', 'status', 'internal_status', 'title',
                       'department', 'priority',)
    filter_fields = ('assigned_to', 'created_by', 'status', 'internal_status', 'department', 'priority', 'client')
    serializer_map = {
        'list': TicketListSerializer,
    }
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, TicketSerializer)

    @action(detail=False, methods=['POST'])
    def get_tickets_for_linking(self, request):
        """
        Lists all tickets except for one
        """
        if 'ticket_id' in request.data:
            ticket_id = request.data.get('ticket_id')
        else:
            raise APIBadRequest(detail=_('Missing ticket id to filter against.'))
        existing_links = TicketLink.objects.filter(ticket__id=ticket_id).values_list('linked_ticket')
        search_value = request.data.get('search', None)
        if search_value:
            filter_param = Q(id__startswith=search_value) | Q(title__startswith=search_value)
            queryset = Ticket.objects.filter(filter_param)
        else:
            queryset = Ticket.objects.all()
        exclude_params = Q(id=ticket_id) | Q(id__in=existing_links)
        queryset = queryset.exclude(exclude_params)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TicketListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TicketListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def reopen_ticket(self, request, pk):
        del pk  # unused
        ticket = self.get_object()
        if ticket.status != TicketStatus.done:
            raise APIBadRequest(_('Ticket is already opened.'))
        ticket.status = TicketStatus.open
        if ticket.internal_status == TicketStatus.done:
            ticket.internal_status = None
        ticket.save()
        TicketUpdate.objects.create(
            ticket=ticket,
            created_by=request.user,
            reply_text='',
            new_status=TicketStatus.open,
        )
        ticket_notifications_dispatcher.ticket_reopened(ticket=ticket)
        return Response(data={
            'detail': _('Ticket successfully reopened.')
        })

    @action(detail=True, methods=['POST'])
    def close_ticket(self, request, pk):
        del pk  # unused
        ticket = self.get_object()
        new_internal_status = None
        if ticket.status == TicketStatus.done:
            raise APIBadRequest(_('Ticket is already closed.'))
        ticket.status = TicketStatus.done
        if ticket.internal_status != TicketStatus.done:
            new_internal_status = TicketStatus.done
            ticket.internal_status = new_internal_status
        ticket.save()
        TicketUpdate.objects.create(
            ticket=ticket,
            created_by=request.user,
            reply_text='',
            new_status=TicketStatus.done,
            new_internal_status=new_internal_status,
        )
        ticket_notifications_dispatcher.ticket_closed(ticket=ticket)
        return Response(data={
            'detail': _('Ticket successfully closed.')
        })

    @action(detail=True, methods=['POST'])
    def add_reply(self, request, pk):
        del pk  # unused
        ticket = self.get_object()
        reply_text = request.data.get('reply_text', None)
        associated_attachments = request.data.get('associated_attachments', None)
        attachment_ids = list()
        if associated_attachments:
            attachment_ids = associated_attachments.strip().split(',')

        new_update = None
        with transaction.atomic():
            if reply_text:
                try:
                    new_update = TicketUpdate.objects.create(
                        ticket=ticket,
                        created_by=request.user,
                        reply_text=reply_text,
                    )
                except Exception as e:
                    if len(attachment_ids):
                        TicketUtils.remove_not_associated_attachments(attachment_ids=attachment_ids)
                    raise APIBadRequest(str(e))

        if new_update:
            # associate attachments
            if len(attachment_ids):
                for attachment_id in attachment_ids:
                    try:
                        attachment = Attachment.objects.get(id=attachment_id)
                        if (not attachment.ticket and not attachment.ticket_note and
                                not attachment.ticket_update and not attachment.email_message):
                            attachment.ticket = ticket
                            attachment.ticket_update = new_update
                            attachment.save()
                        else:
                            if request and request.user:
                                LOG.error('User {} tried to associate a foreign attachment '
                                          'with a newly created ticket reply.'.format(request.user.id))
                            raise ValidationError(
                                detail=_('Cannot associate the attachment to the newly created reply because it is'
                                         ' already linked to another object.')
                            )
                    except Attachment.DoesNotExist:
                        LOG.debug('Could not associate attachment to newly created ticket reply because '
                                  'the attachment does not exist')
                    except ValueError:
                        pass
            ticket_notifications_dispatcher.ticket_updated(ticket=ticket)
            return Response(data={
                'reply_id': new_update.id
            })
        else:
            return Response()

    @action(detail=True, methods=['POST'])
    def add_note(self, request, pk):
        del pk  # unused
        ticket = self.get_object()
        note_text = request.data.get('note_text', None)
        associated_attachments = request.data.get('associated_attachments', None)
        attachment_ids = list()
        if associated_attachments:
            attachment_ids = associated_attachments.strip().split(',')

        with transaction.atomic():
            if note_text:
                try:
                    new_note = TicketNote.objects.create(
                        ticket=ticket,
                        created_by=request.user,
                        note_text=note_text
                    )
                except Exception as e:
                    if len(attachment_ids):
                        TicketUtils.remove_not_associated_attachments(attachment_ids=attachment_ids)
                    raise APIBadRequest(str(e))
                if new_note:
                    # associate attachments
                    if len(attachment_ids):
                        for attachment_id in attachment_ids:
                            try:
                                attachment = Attachment.objects.get(id=attachment_id)
                                if (not attachment.ticket and not attachment.ticket_note and
                                        not attachment.ticket_update and not attachment.email_message):
                                    attachment.ticket = ticket
                                    attachment.ticket_note = new_note
                                    attachment.save()
                                else:
                                    raise ValidationError(
                                        detail=_(
                                            'Cannot associate the attachment to the note because it is already linked'
                                            ' to another object.')
                                    )
                            except Attachment.DoesNotExist:
                                LOG.debug('Could not associate attachment to newly created ticket note because '
                                          'the attachment does not exist')
                            except ValueError:
                                pass
                return Response(data={
                    'note_id': new_note.id
                })
        return Response()

    def create(self, request, *args, **kwargs):
        try:
            resp = super().create(request=request, *args, **kwargs)
            return resp
        except (Exception, ValidationError) as e:
            # if create ticket fails and attachments were added alongside it, remove the attachments from disk and db
            associated_attachment_ids = request.data.get('associated_attachment_ids', None)
            if associated_attachment_ids:
                attachment_ids = associated_attachment_ids.strip().split(',')  # format them as a list
                TicketUtils.remove_not_associated_attachments(attachment_ids=attachment_ids)
            raise e

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        request = serializer.context.get('request', None) if serializer.context else None
        associated_attachment_ids = None
        if 'associated_attachment_ids' in serializer.validated_data:
            # get attachment ids for attachments that need to be associated with the ticket
            associated_attachment_ids = serializer.validated_data.get('associated_attachment_ids')
            del serializer.validated_data['associated_attachment_ids']

        ticket = serializer.save(created_by=self.request.user)

        # format a list of ids of attachments that need to be associated with the ticket
        attachment_ids = []
        if associated_attachment_ids:
            attachment_ids = associated_attachment_ids.strip().split(',')

        # associate attachments with the ticket if they were created at once
        if len(attachment_ids):
            for attachment_id in attachment_ids:
                try:
                    attachment = Attachment.objects.get(id=attachment_id)
                    if (not attachment.ticket and not attachment.ticket_note and not attachment.ticket_update and
                            not attachment.email_message):
                        attachment.ticket = ticket
                        attachment.save()
                    else:
                        if request and request.user:
                            LOG.error(
                                'User {} tried to associate a foreign attachment with a newly created ticket.'.format(
                                    request.user.id
                                )
                            )
                        raise ValidationError(
                            detail=_('Cannot add the attachment you tried to associate to the ticket because it '
                                     'is already linked to an object.')
                        )
                except Attachment.DoesNotExist:
                    LOG.debug(
                        'Could not associate attachment to newly created ticket because the attachment does not exist'
                    )
                except ValueError:
                    pass
        ticket_notifications_dispatcher.ticket_created(ticket=ticket)

    def perform_update(self, serializer):
        prev_ticket = serializer.instance  # type: Ticket
        new_assignee = get_new_or_none(serializer.validated_data, 'assigned_to', prev_ticket.assigned_to)
        new_department = get_new_or_none(serializer.validated_data, 'department', prev_ticket.department)
        new_priority = get_new_or_none(serializer.validated_data, 'priority', prev_ticket.priority)
        new_status = get_new_or_none(serializer.validated_data, 'status', prev_ticket.status)
        new_internal_status = get_new_or_none(serializer.validated_data, 'internal_status', prev_ticket.internal_status)
        new_client = get_new_or_none(serializer.validated_data, 'client', prev_ticket.client)
        new_cc = get_new_or_none(serializer.validated_data, 'cc_recipients', prev_ticket.cc_recipients)
        new_cc_data = TicketUtils.add_new_addresses_to_cc(prev_ticket.cc_recipients, new_cc) if new_cc else None
        description_changed = get_new_or_none(
            serializer.validated_data, 'description', prev_ticket.description
        ) is not None
        title_changed = get_new_or_none(serializer.validated_data, 'title', prev_ticket.title) is not None

        new_update = None
        with transaction.atomic():
            if (new_assignee or new_status or new_internal_status or description_changed or
                    title_changed or new_department or new_priority or new_client or new_cc):
                new_update = TicketUpdate.objects.create(
                    ticket=prev_ticket,
                    created_by=self.request.user,
                    new_department=new_department,
                    new_status=new_status,
                    new_priority=new_priority,
                    new_internal_status=new_internal_status,
                    new_assignee=new_assignee,
                    description_changed=description_changed,
                    title_changed=title_changed,
                    new_client=new_client,
                    new_cc=new_cc_data['differences'] if new_cc_data else None,
                )

            serializer.save()

        if new_update:
            ticket_notifications_dispatcher.ticket_updated(ticket=prev_ticket)

    def perform_destroy(self, instance):
        attachment_storage = AttachmentsStorage.get_attachments_storage()
        for attachment in instance.attachments.all():
            attachment_storage.remove_attachment_from_disk(disk_file=attachment.disk_file)
        instance.delete()

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        ticket_id = request.query_params.get('ticket_id', None)
        signature = None    # type: StaffSignature
        if ticket_id:
            ticket = Ticket.objects.filter(id=ticket_id).first()
            if not ticket:
                raise APIBadRequest(_('Ticket with id {} not found.').format(ticket_id))
            signature = StaffSignature.objects.filter(
                user=request.user,
                department=ticket.department
            ).first()
        if not ticket_id or not signature:
            signature = StaffSignature.objects.filter(
                user=request.user,
                department=None
            ).first()
        signature_content = signature.content if signature else None

        return Response(data={
            'statuses': TicketStatus.status_map,
            'internal_statuses': TicketStatus.internal_status_map,
            'priorities': TicketPriority.priority_map,
            'MAX_TICKET_ATTACHMENT_SIZE': getattr(settings, 'MAX_TICKET_ATTACHMENT_SIZE'),
            'user_signature': signature_content,
        })

    @action(detail=False, methods=['get'])
    def get_current_user_tickets_count(self, request):
        """Fetches tickets assigned to the logged in user and tickets that have no assignee based on internal status"""
        user = request.user
        filter_param = Q(assigned_to=user) | Q(assigned_to=None)
        ticket_count = Ticket.objects.filter(filter_param).exclude(internal_status=TicketStatus.done).count()
        return Response({'count': ticket_count})

    @action(detail=False, methods=['GET'])
    def get_client_related_tickets(self, request):
        """Fetches tickets related to a given client"""
        client_id = request.query_params.get('client_id', None)
        client = Client.objects.filter(id=client_id).first() if client_id else None  # type: Client
        if client:
            related_tickets = Ticket.objects.filter(client=client).order_by('-created_at')
            page = self.paginate_queryset(related_tickets)
            if page is not None:
                serializer = TicketBriefSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = TicketBriefSerializer(related_tickets, many=True)
            return Response(serializer.data)
        return Response({
            'detail': _('Client not found for getting tickets')},
            status=HTTP_422_UNPROCESSABLE_ENTITY
        )

    @action(detail=False, methods=['GET'])
    def get_user_related_tickets(self, request):
        """Fetches tickets related to a given user"""
        user_id = request.query_params.get('user_id', None)
        user = AppUser.objects.filter(id=user_id).first() if user_id else None  # type: AppUser
        if user:
            user_clients = user.clients.all()
            if user_clients:
                filtering_params = Q(created_by=user) | Q(client__in=user_clients)
            else:
                filtering_params = Q(created_by=user)
            related_tickets = Ticket.objects.filter(filtering_params).order_by('-created_at')
            page = self.paginate_queryset(related_tickets)
            if page is not None:
                serializer = TicketBriefSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = TicketBriefSerializer(related_tickets, many=True)
            return Response(serializer.data)
        return Response({
            'detail': _('User not found when getting related tickets')},
            status=HTTP_422_UNPROCESSABLE_ENTITY
        )
