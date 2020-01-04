import logging
from datetime import timedelta
from os import environ
from os.path import abspath, dirname
import sys

import django
from django.utils.timezone import now as utcnow

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))

sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

LOG = logging.getLogger(__name__)

from fleio.core.models import Client  # noqa
from fleio.openstack.api.identity import IdentityAdminApi  # noqa
from fleio.openstack.configuration import OpenstackSettings  # noqa
from fleio.openstack.images.api import Images  # noqa
from fleio.openstack.models import Image  # noqa


def run():
    os_admin_api = IdentityAdminApi()

    for client in Client.objects.all():  # type: Client
        try:
            LOG.debug('Cleaning up for client {}'.format(client))

            if not client.first_project:
                LOG.debug('Skipping client without project ...')
                continue

            openstack_settings = OpenstackSettings.for_client(client=client)
            if openstack_settings.auto_cleanup_images:
                max_create_date = utcnow() - timedelta(days=openstack_settings.auto_cleanup_number_of_days)
                images_to_cleanup = Image.objects.filter(
                    disk_format__in=openstack_settings.auto_cleanup_image_types,
                    created_at__lte=max_create_date,
                    project=client.first_project,
                ).all()

                for image in images_to_cleanup:
                    os_api = Images(api_session=os_admin_api.session)
                    os_image = os_api.get(image=image)
                    # TODO: implement protected image deletion
                    if not image.protected:
                        os_image.delete()
        except Exception as e:
            LOG.exception('Error processing client {} - {}'.format(client, e))


if __name__ == '__main__':
    run()
