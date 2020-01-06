from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from plugins.tickets.models.attachment import Attachment
from plugins.tickets.staff.tickets.attachments_serializers import AttachmentSerializer, AttachmentSerializerDetail

from rest_framework import mixins, viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from fleio.core.exceptions import APIBadRequest
from rest_framework.decorators import action

from fleio.core.drf import EndUserOnly
from fleio.core.filters import CustomFilter

from plugins.tickets.common.attachments_storage import AttachmentsStorage
from plugins.tickets.common.uploadhandler import CustomTemporaryFileUploadHandler


class TicketAttachmentsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)

    serializer_map = {
        'retrieve': AttachmentSerializerDetail,
    }

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, AttachmentSerializer)

    def dispatch(self, request, *args, **kwargs):
        request.upload_handlers.insert(0, CustomTemporaryFileUploadHandler(request))
        return super(TicketAttachmentsViewSet, self).dispatch(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            attachment = Attachment.objects.get(id=kwargs['pk'])
            # Check if the ticket related to the attachment is also related to the enduser
            ticket = attachment.ticket
            clients = request.user.clients.all()
            if (ticket.created_by == request.user or ticket.client in clients) and attachment.ticket_note is None:
                return Response(data=AttachmentSerializerDetail(attachment).data)
            else:
                raise PermissionDenied(_('You do not have the permission to access this attachment'))
        except Attachment.DoesNotExist:
            raise NotFound()

    @action(detail=True, methods=['GET'])
    def download_file(self, request, pk):
        del pk  # unused
        attachment = self.get_object()
        ticket = attachment.ticket
        clients = request.user.clients.all()
        if (ticket.created_by == request.user or ticket.client in clients) and attachment.ticket_note is None:
            attachment_storage = AttachmentsStorage.get_attachments_storage()
            file = attachment_storage.load_attachment(attachment.disk_file)
            response = HttpResponse(file, content_type=attachment.content_type)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(attachment.file_name)
            return response
        else:
            raise PermissionDenied(_('You do not have the permission to access this attachment'))

    @action(detail=True, methods=['GET'])
    def load_file(self, request, pk):
        del pk  # unused
        attachment = self.get_object()
        ticket = attachment.ticket
        clients = request.user.clients.all()
        if (ticket.created_by == request.user or ticket.client in clients) and attachment.ticket_note is None:
            attachment_storage = AttachmentsStorage.get_attachments_storage()
            file = attachment_storage.load_attachment(attachment.disk_file)
            response = HttpResponse(file, content_type=attachment.content_type)
            return response
        else:
            raise PermissionDenied(_('You do not have the permission to access this attachment'))

    def get_queryset(self):
        queryset = Attachment.objects.all()
        # remove attachments related to ticket notes as enduser cannot manage notes
        queryset = queryset.exclude(ticket_note__isnull=False)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.FILES.get('data'):
            error_map = {
                'FILE_TOO_BIG': _('Could not upload attachment. File size is too large.'),
                'NO_SPACE_ON_DISK': _('Could not upload attachment. Not enough free space on destination file system.')
            }
            if self.request.META.get('FILE_TOO_BIG'):
                raise APIBadRequest(detail=error_map.get('FILE_TOO_BIG'))
            elif self.request.META.get('NO_SPACE_ON_DISK'):
                raise APIBadRequest(detail=error_map.get('NO_SPACE_ON_DISK'))
            else:
                raise APIBadRequest(detail='Missing data')

        attachment_data = request.FILES.get('data').read()
        params = {
            'file_name': request.POST.get('file_name'),
            'content_type': request.FILES.get('data').content_type
        }
        attachment_storage = AttachmentsStorage.get_attachments_storage()
        disk_file_name = attachment_storage.create_disk_file_name(params['file_name'])
        params['disk_file'] = disk_file_name
        attachment_storage.save_attachment(disk_file_name=disk_file_name, attachment_data=attachment_data)
        obj = Attachment.objects.create(**params)
        return Response(data=AttachmentSerializerDetail(obj).data)
