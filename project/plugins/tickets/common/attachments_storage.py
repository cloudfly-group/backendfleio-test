import logging
import os
from typing import Optional
import uuid

from django.conf import settings


ATTACHMENTS_DIR = settings.ATTACHMENTS_DIR if settings.ATTACHMENTS_DIR else '/var/fleio/attachments'

ATTACHMENTS_STORAGE = None

LOG = logging.getLogger(__name__)


class AttachmentsStorage(object):

    def __init__(self):
        self.is_initialized = True
        try:
            parent_dir = os.path.dirname(ATTACHMENTS_DIR)
            parent_stat = os.stat(parent_dir)

            if not os.path.exists(ATTACHMENTS_DIR):
                os.mkdir(ATTACHMENTS_DIR)
                stats = os.stat(ATTACHMENTS_DIR)
                if stats.st_uid != parent_stat.st_uid:
                    os.chown(ATTACHMENTS_DIR, parent_stat.st_uid, parent_stat.st_gid)

            for i in range(0, 255):
                sub_dir_name = '{:02x}'.format(i)
                sub_dir_path = os.path.join(ATTACHMENTS_DIR, sub_dir_name)
                if not os.path.exists(sub_dir_path):
                    os.mkdir(sub_dir_path)
                    stats = os.stat(ATTACHMENTS_DIR)
                    if stats.st_uid != parent_stat.st_uid:
                        os.chown(sub_dir_path, parent_stat.st_uid, parent_stat.st_gid)
        except Exception as e:
            LOG.exception('Failed to initialize attachment storage: {}'.format(e))
            self.is_initialized = False

    @staticmethod
    def get_attachments_storage() -> 'AttachmentsStorage':
        global ATTACHMENTS_STORAGE
        if ATTACHMENTS_STORAGE is None:
            try:
                ATTACHMENTS_STORAGE = AttachmentsStorage()
            except Exception as e:
                del e  # unused
        if ATTACHMENTS_STORAGE.is_initialized is False:
            try:
                ATTACHMENTS_STORAGE = AttachmentsStorage()
            except Exception as e:
                del e  # unused
        return ATTACHMENTS_STORAGE

    @staticmethod
    def create_disk_file_name(file_name: str):
        disk_file_name = '{}_{}'.format(uuid.uuid4(), file_name)
        return disk_file_name

    @staticmethod
    def get_attachment_path(disk_file_name: str):
        sub_dir_name = disk_file_name[:2]
        file_path = os.path.join(ATTACHMENTS_DIR, sub_dir_name, disk_file_name)
        return file_path

    def save_attachment(self, disk_file_name: str, attachment_data: bytes):
        if not self.is_initialized:
            LOG.error('Cannot save attachment {} because storage is not initialized', disk_file_name)
            return

        try:
            disk_path = self.get_attachment_path(disk_file_name=disk_file_name)
            with open(disk_path, 'wb') as attachment_file:
                attachment_file.write(bytearray(attachment_data))
            os.chmod(disk_path, 444)
        except Exception as e:
            LOG.exception('Exception when saving attachment: {}', e)

    def remove_attachment_from_disk(self, disk_file: str):
        """Removes the attachment file from the the disk"""
        path = self.get_attachment_path(disk_file)
        try:
            os.remove(path=path)
        except FileNotFoundError:
            pass

    def load_attachment(self, disk_file_name: str) -> Optional[bytes]:
        if not self.is_initialized:
            LOG.error('Cannot load attachment {} because storage is not initialized', disk_file_name)
            return None
        try:
            disk_path = self.get_attachment_path(disk_file_name=disk_file_name)
            with open(disk_path, 'rb') as attachment_file:
                return attachment_file.read()
        except Exception as e:
            LOG.exception('Exception when loading attachment: {}', e)
