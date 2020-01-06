import logging
from os import chown

from os import mkdir
from os import path
from os import stat
from shutil import copyfile

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fleio.core.exceptions import ForbiddenException
from fleio.core.features import staff_active_features
from fleio.core.models import CustomCode
from fleio.core.models.custom_code import CodeInsertionPoints
from fleio.core.models.custom_code import FrontendFileTypes

LOG = logging.getLogger(__name__)

UNMODIFIED_INDEX_MARKER = '<!-- unmodified -->'


class IndexManager(object):
    class IndexUpdateException(Exception):
        def __init__(self, detail: str):
            self.detail = detail

    def __init__(self):
        self.vanilla_staff_index_path = path.join(settings.FRONTEND_UPDATES_STAFF_DIR, 'index.html')
        self.updated_staff_index_path = path.join(settings.FRONTEND_UPDATES_STAFF_DIR, 'index_updated.html')
        self.vanilla_site_index_path = path.join(settings.FRONTEND_UPDATES_SITE_DIR, 'index.html')
        self.updated_site_index_path = path.join(settings.FRONTEND_UPDATES_SITE_DIR, 'index_updated.html')

        self.local_frontend_staff_index_path = path.join(settings.FRONTEND_STAFF_DIR, 'index.html')
        self.local_frontend_site_index_path = path.join(settings.FRONTEND_SITE_DIR, 'index.html')

        self.create_update_directories()

    @staticmethod
    def create_update_directories():
        try:
            parent_dir = path.dirname(settings.FRONTEND_UPDATES_DIR)
            parent_stat = stat(parent_dir)

            if not path.isdir(settings.FRONTEND_UPDATES_DIR):
                mkdir(settings.FRONTEND_UPDATES_DIR)
                dir_stat = stat(settings.FRONTEND_UPDATES_DIR)
                if dir_stat.st_uid != parent_stat.st_uid:
                    chown(settings.FRONTEND_UPDATES_DIR, parent_stat.st_uid, parent_stat.st_gid)

            if not path.isdir(settings.FRONTEND_UPDATES_STAFF_DIR):
                mkdir(settings.FRONTEND_UPDATES_STAFF_DIR)
                dir_stat = stat(settings.FRONTEND_UPDATES_STAFF_DIR)
                if dir_stat.st_uid != parent_stat.st_uid:
                    chown(settings.FRONTEND_UPDATES_STAFF_DIR, parent_stat.st_uid, parent_stat.st_gid)

            if not path.isdir(settings.FRONTEND_UPDATES_SITE_DIR):
                mkdir(settings.FRONTEND_UPDATES_SITE_DIR)
                dir_stat = stat(settings.FRONTEND_UPDATES_SITE_DIR)
                if dir_stat.st_uid != parent_stat.st_uid:
                    chown(settings.FRONTEND_UPDATES_SITE_DIR, parent_stat.st_uid, parent_stat.st_gid)
        except Exception as e:
            LOG.exception('Exception when creating update directories: {}'.format(e))

    def is_local_frontend(self):
        return path.isfile(self.local_frontend_staff_index_path) and path.isfile(self.local_frontend_site_index_path)

    def has_vanilla_indexes(self):
        return path.isfile(self.vanilla_staff_index_path) and path.isfile(self.vanilla_site_index_path)

    def has_updated_indexes(self):
        return path.isfile(self.updated_staff_index_path) and path.isfile(self.updated_site_index_path)

    @staticmethod
    def copy_unmodified_file(source_path, destination_path):
        with open(source_path, 'r', encoding='utf-8') as local_index:
            contents = local_index.read()
            if UNMODIFIED_INDEX_MARKER in contents:
                copyfile(source_path, destination_path)

    def update_vanilla_indexes(self):
        if self.is_local_frontend():
            self.copy_unmodified_file(self.local_frontend_staff_index_path, self.vanilla_staff_index_path)
            self.copy_unmodified_file(self.local_frontend_site_index_path, self.vanilla_site_index_path)

    @staticmethod
    def generate_updated_index(vanilla_index_path, updated_index_path, frontend_file_type):
        with open(vanilla_index_path, 'r', encoding='utf-8') as vanilla_index:
            contents = vanilla_index.read()
            contents = contents.replace(UNMODIFIED_INDEX_MARKER, '')
            for custom_code in CustomCode.objects.filter(active=True, frontend_file_type=frontend_file_type):
                marker = CodeInsertionPoints.insertion_point_to_marker_map[custom_code.insertion_point]
                code = custom_code.code.strip()
                if len(code) > 0:
                    contents = contents.replace(marker, code)

        with open(updated_index_path, 'w+', encoding='utf-8') as updated_index:
            updated_index.write(contents)

    def generate_updates_indexes(self):
        if self.has_vanilla_indexes():
            self.generate_updated_index(
                self.vanilla_staff_index_path,
                self.updated_staff_index_path,
                FrontendFileTypes.staff_index
            )
            self.generate_updated_index(
                self.vanilla_site_index_path,
                self.updated_site_index_path,
                FrontendFileTypes.enduser_index
            )

    def update_local_frontend(self):
        copyfile(self.updated_staff_index_path, self.local_frontend_staff_index_path)
        copyfile(self.updated_site_index_path, self.local_frontend_site_index_path)

    def update_frontend(self):
        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        if not self.is_local_frontend():
            raise IndexManager.IndexUpdateException(detail=_('Cannot find frontend instalation'))

        self.update_vanilla_indexes()

        if not self.has_vanilla_indexes():
            raise IndexManager.IndexUpdateException(detail=_('No unmodified index.html file available'))

        self.generate_updates_indexes()

        if not self.has_updated_indexes():
            raise IndexManager.IndexUpdateException(detail=_('Failed to generate updated index.html file'))

        self.update_local_frontend()
