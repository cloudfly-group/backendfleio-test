import os

from django.core.files.uploadhandler import MemoryFileUploadHandler, StopUpload
from django.conf import settings

from plugins.tickets.common.attachments_storage import AttachmentsStorage


class CustomTemporaryFileUploadHandler(MemoryFileUploadHandler):
    """
    Upload handler that extends MemoryFileUploadHandler adding file size and disk space checks
    """

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        """
        Use the content_length to signal whether or not this handler should be
        used.
        """
        AttachmentsStorage.get_attachments_storage()
        statvfs = os.statvfs(getattr(settings, 'ATTACHMENTS_DIR'))
        # Number of free bytes that ordinary users are allowed to use
        free_space = statvfs.f_frsize * statvfs.f_bavail
        # Limit upload options
        if content_length > getattr(settings, 'MAX_TICKET_ATTACHMENT_SIZE'):
            self.request.META['FILE_TOO_BIG'] = True
        # Don't allow uploads if there is not enough space on the server disk
        if free_space < getattr(settings, 'FREE_DISK_SPACE_LIMIT') or free_space < content_length:
            self.request.META['NO_SPACE_ON_DISK'] = True
        # If the post is too large, we cannot use the Memory handler.
        self.activated = content_length <= settings.FILE_UPLOAD_MAX_MEMORY_SIZE

    def receive_data_chunk(self, raw_data, start):
        """Add the data to the BytesIO file."""
        if self.request.META.get('FILE_TOO_BIG'):
            raise StopUpload(connection_reset=True)
        if self.request.META.get('NO_SPACE_ON_DISK'):
            raise StopUpload(connection_reset=True)
        if self.activated:
            self.file.write(raw_data)
        else:
            if start > getattr(settings, 'MAX_TICKET_ATTACHMENT_SIZE'):
                self.request.META['FILE_TOO_BIG'] = True
                raise StopUpload(connection_reset=True)
            return raw_data
