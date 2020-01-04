import logging

from cinderclient import exceptions as cinder_exceptions
from django.conf import settings

from fleio.celery import app
from fleio.openstack.api.cinder import cinder_client
from fleio.openstack.models import Volume
from fleiostaff.openstack.osadminapi import OSAdminApi

LOG = logging.getLogger(__name__)


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Volume extra details synchronization',
    resource_type='Volume',
)
def sync_volume_extra_details(self, volume_id, region_name):
    del self  # unused
    os_api = OSAdminApi()
    cc = cinder_client(api_session=os_api.get_session(), region_name=region_name)
    try:
        volume_from_os = cc.volumes.get(volume_id)
    except cinder_exceptions.NotFound:
        pass
    else:
        db_volume = Volume.objects.filter(id=volume_id).first()
        if db_volume and volume_from_os:
            if volume_from_os.bootable == 'true':
                db_volume.bootable = True
            if volume_from_os.bootable == 'false':
                db_volume.bootable = False
            db_volume.save()
