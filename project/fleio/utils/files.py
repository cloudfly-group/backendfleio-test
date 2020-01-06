from os import mkdir
from os import path
from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile


def save_uploaded_file(source_file: TemporaryUploadedFile):
    if not path.isdir(settings.FLEIO_TEMP_DIR):
        mkdir(settings.FLEIO_TEMP_DIR)
    temp_file_name = path.join(settings.FLEIO_TEMP_DIR, str(uuid4()))
    with open(temp_file_name, 'wb+') as destination_file:
        for chunk in source_file.chunks():
            destination_file.write(chunk)

    return temp_file_name
