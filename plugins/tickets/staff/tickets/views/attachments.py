from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from plugins.tickets.models.attachment import Attachment
from plugins.tickets.staff.tickets.attachments_serializers import AttachmentSerializer, AttachmentSerializerDetail

from rest_framework import mixins, viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action

from fleio.core.exceptions import APIBadRequest
from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter

from plugins.tickets.common.attachments_storage import AttachmentsStorage
from plugins.tickets.common.uploadhandler import CustomTemporaryFileUploadHandler


class TicketAttachmentsViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    queryset = Attachment.objects.all()

    serializer_map = {
        'retrieve': AttachmentSerializerDetail,
    }

    def dispatch(self, request, *args, **kwargs):
        request.upload_handlers.insert(0, CustomTemporaryFileUploadHandler(request))
        return super(TicketAttachmentsViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, AttachmentSerializer)

    @action(detail=True, methods=['GET'])
    def download_file(self, request, pk):
        del request, pk  # unused
        file_data = self.get_object()
        attachment_storage = AttachmentsStorage.get_attachments_storage()
        file = attachment_storage.load_attachment(file_data.disk_file)
        response = HttpResponse(file, content_type=file_data.content_type)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_data.file_name)
        return response

    @action(detail=True, methods=['GET'])
    def load_file(self, request, pk):
        del request, pk  # unused
        file_data = self.get_object()
        attachment_storage = AttachmentsStorage.get_attachments_storage()
        file = attachment_storage.load_attachment(file_data.disk_file)
        response = HttpResponse(file, content_type=file_data.content_type)
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file_data.file_name)
        return response

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
