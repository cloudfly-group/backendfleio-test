import logging

from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _

from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from fleio.core.drf import EndUserOnly
from fleio.core.filters import CustomFilter
from fleio.core.exceptions import APIBadRequest

from fleio.utils.collections import get_new_or_none

from plugins.tickets.common.ticket_notification_dispatcher import ticket_notifications_dispatcher
from plugins.tickets.common.tickets_utils import TicketUtils
from plugins.tickets.common.tickets_filters import TicketIdSearchFilter

from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket_update import TicketUpdate
from plugins.tickets.models.ticket import TicketPriority
from plugins.tickets.models.ticket import TicketStatus
from plugins.tickets.models.attachment import Attachment
from fleio.billing.models.service import Service

from plugins.tickets.enduser.tickets.serializers import TicketSerializer
from plugins.tickets.enduser.tickets.serializers import TicketUpdateUpdateSerializer
from plugins.tickets.enduser.tickets.serializers import TicketListSerializer
from plugins.tickets.enduser.tickets.serializers import TicketCreateSerializer
from fleio.billing.services.serializers import ServiceBriefSerializer


LOG = logging.getLogger(__name__)


class TicketUpdateViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    serializer_class = TicketUpdateUpdateSerializer
    queryset = TicketUpdate.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            update = TicketUpdate.objects.get(id=kwargs['pk'])
            # Check if the ticket related to the update is also related to the enduser
            ticket = update.ticket
            clients = request.user.clients.all()
            if ticket.created_by == request.user or ticket.client in clients:
                return Response(data=TicketUpdateUpdateSerializer(update).data)
            else:
                raise PermissionDenied(_('You do not have the permission to access this ticket update'))
        except TicketUpdate.DoesNotExist:
            raise NotFound()


class TicketsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TicketSerializer
    permission_classes = (EndUserOnly,)
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
    ordering_fields = ('created_at', 'created_by', 'status', 'title', 'department',)
    filter_fields = ('created_by', 'status', 'department', 'client')
    serializer_map = {
        'list': TicketListSerializer,
        'create': TicketCreateSerializer
    }

    def get_queryset(self):
        created_by = Q(**{'created_by': self.request.user})
        client = Q(**{'client__in': self.request.user.clients.all()})
        final = created_by | client
        return Ticket.objects.filter(final)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, TicketSerializer)

    @action(detail=False, methods=['get'])
    def get_current_user_tickets_count(self, request):
        user = request.user
        user_clients = user.clients.all()
        params = Q(client__in=user_clients) | Q(created_by=user)
        qs = Ticket.objects.filter(params)
        qs = qs.exclude(status=TicketStatus.done)
        ticket_count = qs.count()
        return Response({'count': ticket_count})

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
        if ticket.internal_status is None:
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
                                detail=_('Could not associate the attachment to newly created ticket reply because '
                                         'it is already linked to another object.')
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

    def create(self, request, *args, **kwargs):
        try:
            resp = super().create(request=request, *args, **kwargs)
            return resp
        except ValidationError as e:
            # if create ticket fails and attachments were added alongside it, remove the attachments from disk and db
            attachment_ids = request.data.get('associated_attachment_ids', None)
            if attachment_ids:
                attachment_ids = attachment_ids.strip().split(',')  # format them as a list
                TicketUtils.remove_not_associated_attachments(attachment_ids=attachment_ids)
            raise e

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        request = serializer.context.get('request', None) if serializer.context else None
        associated_attachment_ids = None
        if 'associated_attachment_ids' in serializer.validated_data:
            # get attachment ids for attachments that need to be associated with the ticket
            associated_attachment_ids = serializer.validated_data.get('associated_attachment_ids', None)
            del serializer.validated_data['associated_attachment_ids']

        ticket = serializer.save(
            created_by=self.request.user,
            priority=TicketPriority.medium,
            status=TicketStatus.open,
        )
        attachment_ids = list()
        if associated_attachment_ids:
            attachment_ids = associated_attachment_ids.strip().split(',')

        # associate attachment with the ticket if they were created at once
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
                            detail=_('Could not associate the attachment to the newly created ticket because it is '
                                     'already linked to another object.')
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
        new_department = get_new_or_none(serializer.validated_data, 'department', prev_ticket.department)
        new_status = get_new_or_none(serializer.validated_data, 'status', prev_ticket.status)
        new_client = get_new_or_none(serializer.validated_data, 'client', prev_ticket.client)
        new_cc = get_new_or_none(serializer.validated_data, 'cc_recipients', prev_ticket.cc_recipients)
        new_cc_data = TicketUtils.add_new_addresses_to_cc(prev_ticket.cc_recipients, new_cc) if new_cc else None
        description_changed = get_new_or_none(
            serializer.validated_data, 'description', prev_ticket.description
        ) is not None
        title_changed = get_new_or_none(serializer.validated_data, 'title', prev_ticket.title) is not None

        new_update = None
        with transaction.atomic():
            if (new_status or description_changed or title_changed or new_department or
                    new_client or new_cc):
                new_update = TicketUpdate.objects.create(
                    ticket=prev_ticket,
                    created_by=self.request.user,
                    new_department=new_department,
                    new_status=new_status,
                    description_changed=description_changed,
                    title_changed=title_changed,
                    new_client=new_client,
                    new_cc=new_cc_data['differences'] if new_cc_data else None,
                )

            serializer.save()

        if new_update:
            ticket_notifications_dispatcher.ticket_updated(ticket=prev_ticket)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        clients = request.user.clients.all()
        service_queryset = Service.objects.filter(client__in=clients)
        serialized_services = ServiceBriefSerializer(instance=service_queryset, many=True).data
        return Response(data={
            'MAX_TICKET_ATTACHMENT_SIZE': getattr(settings, 'MAX_TICKET_ATTACHMENT_SIZE'),
            'services': serialized_services,
        })
