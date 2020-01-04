import subprocess
from io import BytesIO
import logging
import os
from os import path

import requests
import tempfile

from django.conf import settings
from fleio.celery import app
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.api.glance import glance_client


LOG = logging.getLogger(__name__)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Import image from url', resouce_type='Image')
def import_image_from_url(self, image_id, url, region_name):
    """
    Upload an image data to Glance as admin, by downloading it first from a URL.
    Do not use this task in user views.
    """
    del self  # unused

    admin_api = IdentityAdminApi()
    gc = glance_client(api_session=admin_api.session, region_name=region_name)
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        temp_image_dir = getattr(settings, 'OPENSTACK_IMAGE_TEMP_DIR', None)
        with tempfile.TemporaryFile(dir=temp_image_dir, prefix='glance_') as temp_image_file:
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    temp_image_file.write(chunk)
            temp_image_file.seek(0)  # Go to the beginning to be able to read it
            gc.images.upload(image_id=image_id, image_data=temp_image_file)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Import image from file', resource_type='Image')
def import_image_from_file(self, image_id, region_name, file_path):
    """
    Upload an image data to Glance as admin.
    Do not use this task in user views.
    """
    del self  # unused

    LOG.info('Uploading image {} in region {} from file {}'.format(
        image_id, region_name, file_path,
    ))

    admin_api = IdentityAdminApi()
    gc = glance_client(api_session=admin_api.session, region_name=region_name)
    with open(file_path, mode="rb") as temp_file:
        try:
            gc.images.upload(image_id=image_id, image_data=temp_file)
        finally:
            filename = str(temp_file.name)
            os.remove(filename)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Import zero filled image', resource_type='Image')
def upload_zero_filled_image(self, image_id, region_name, length_in_bytes=0):
    """
    Upload an image data to Glance as admin.
    Do not use this task in user views.
    """
    del self  # unused

    admin_api = IdentityAdminApi()
    gc = glance_client(api_session=admin_api.session, region_name=region_name)
    buffer = BytesIO(bytearray(length_in_bytes))
    gc.images.upload(image_id=image_id, image_data=buffer)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Upload empty qcow2 image', resource_type='Image')
def upload_empty_qcow2_image(self, image_id, region_name, disk_size_in_bytes=0):
    """
    Upload an image data to Glance as admin.
    Do not use this task in user views.
    """
    del self  # unused

    # ensure we have an empty qcow2 file to upload
    if not path.isdir(settings.FLEIO_TEMP_DIR):
        os.mkdir(settings.FLEIO_TEMP_DIR)
    qcow2_file_path = path.join(settings.FLEIO_TEMP_DIR, 'boot_from_iso_img.qcow2')
    if not path.isfile(qcow2_file_path):
        subprocess.call(['qemu-img', 'create', '-f', 'qcow2', qcow2_file_path, str(disk_size_in_bytes)])

    if not path.isfile(qcow2_file_path):
        raise IOError('Failed to initialize temporary qcow2 file')

    admin_api = IdentityAdminApi()
    gc = glance_client(api_session=admin_api.session, region_name=region_name)
    with open(qcow2_file_path, mode="rb") as temp_file:
        gc.images.upload(image_id=image_id, image_data=temp_file)
