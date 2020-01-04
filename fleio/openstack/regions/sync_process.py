import logging

from fleio.openstack.api import identity
from fleio.openstack.models import OpenstackRegion

LOG = logging.getLogger(__name__)


def sync_regions(auth_cache=None):
    synced_regions = list()

    kc = identity.IdentityAdminApi(request_session=auth_cache).client
    for keystone_region in kc.regions.list():
        synced_regions.append(keystone_region.id)
        db_region, created = OpenstackRegion.objects.get_or_create(
            id=keystone_region.id,
            defaults={'description': keystone_region.description}
        )
        if created:
            LOG.info('Adding region {} to fleio database'.format(keystone_region.id))

    OpenstackRegion.objects.exclude(id__in=synced_regions).delete()
    return OpenstackRegion.objects.all()
