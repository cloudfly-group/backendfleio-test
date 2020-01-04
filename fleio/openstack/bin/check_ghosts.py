import logging
import os
from os import environ
from os.path import abspath, dirname
import sys

import django

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))

sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

LOG = logging.getLogger(__name__)

from fleio.osbilling.models import ResourceUsageLog  # noqa
from fleio.openstack.models import Instance  # noqa
from fleio.openstack.models import Image  # noqa
from fleio.openstack.models import Volume  # noqa
from django.utils.timezone import now as utcnow  # noqa

RESOURCE_MAP = {
    'instance': Instance,
    'image': Image,
    'volume': Volume,
}

GHOST_RESOURCES_DIR = '/var/fleio/ghost_resources'


def _generate_ghosts_log(resource_name, parent_stat):
    model = RESOURCE_MAP.get(resource_name)
    now = utcnow()
    date_dir_name = '{}-{}-{}'.format(now.year, now.month, now.day)
    date_dir_path = '{}/{}'.format(GHOST_RESOURCES_DIR, date_dir_name)
    if not os.path.exists(date_dir_path):
        os.mkdir(date_dir_path)
        stats = os.stat(date_dir_path)
        if stats.st_uid != parent_stat.st_uid:
            os.chown(date_dir_path, parent_stat.st_uid, parent_stat.st_gid)
    with open('{}/{}'.format(date_dir_path, resource_name), 'w') as log_file:
        resource_usage_logs = ResourceUsageLog.objects.filter(resource_type=resource_name, end=None)
        total_count = 0
        for resource_usage_log in resource_usage_logs:
            try:
                model.objects.get(id=resource_usage_log.resource_uuid)
            except model.DoesNotExist:
                log_file.write(
                    'Not found resource with uuid: {} in db, but it has a resource usage log '
                    'that has no end date.\n'.format(resource_usage_log.resource_uuid)
                )
                total_count = total_count + 1
        log_file.write('TOTAL: {}\n'.format(total_count))
    return '{}/{}'.format(date_dir_path, resource_name)


def run(resource_name=None):
    parent_dir = os.path.dirname(GHOST_RESOURCES_DIR)
    parent_stat = os.stat(parent_dir)

    if not os.path.exists(GHOST_RESOURCES_DIR):
        os.mkdir(GHOST_RESOURCES_DIR)
        stats = os.stat(GHOST_RESOURCES_DIR)
        if stats.st_uid != parent_stat.st_uid:
            os.chown(GHOST_RESOURCES_DIR, parent_stat.st_uid, parent_stat.st_gid)
    if resource_name:
        generated_path = _generate_ghosts_log(resource_name=resource_name, parent_stat=parent_stat)
        return [generated_path, ]
    else:
        generated_paths = []
        for resource_name in RESOURCE_MAP:
            generated_path = _generate_ghosts_log(resource_name=resource_name, parent_stat=parent_stat)
            generated_paths.append(generated_path)
        return generated_paths


if __name__ == '__main__':
    if len(sys.argv) > 1:
        resource_type = sys.argv[1]
        if RESOURCE_MAP.get(resource_type, None) is None:
            sys.exit('Invalid resource type.')
        paths = run(resource_name=resource_type)
    else:
        paths = run()
    message = 'Ghost resources log finished generating and can be found at:\n'
    for path in paths:
        message = message + path + '\n'
    sys.exit(message)
