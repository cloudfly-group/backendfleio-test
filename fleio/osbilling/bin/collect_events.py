from __future__ import unicode_literals

import logging
import sys
from os import environ
from os.path import abspath, dirname

import django

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))
sys.path.append(fleio_path)

environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleio.core.models import Client
from fleio.openstack.settings import plugin_settings
from fleio.osbilling.collectors.collectors import EventsCollector

LOG = logging.getLogger(__name__)


if __name__ == '__main__':
    EvC = EventsCollector()
    for client in Client.objects.all():
        openstack_project = client.first_project
        if openstack_project is not None:
            EvC.collect(project_id=openstack_project.project_id, region_name=plugin_settings.DEFAULT_REGION)
        else:
            LOG.debug('Skipping client with no OpenStack project: {}'.format(client))
