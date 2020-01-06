import logging
from typing import Optional
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets

from fleio.core.drf import EndUserOnly
from fleio.openstack import exceptions
from fleio.openstack.models import OpenstackRegion
from fleio.openstack.serializers.regions import RegionSerializer
from fleio.openstack.settings import plugin_settings

LOG = logging.getLogger(__name__)


def get_regions(request, filter_for: Optional[str] = None, for_end_user: bool = False):
    try:
        kwargs = {}
        if filter_for:
            kwargs['enable_{}'.format(filter_for)] = True
        if for_end_user:
            regions = OpenstackRegion.objects.enabled_for_enduser().filter(**kwargs).all()
        else:
            regions = OpenstackRegion.objects.enabled().filter(**kwargs).all()
    except Exception as e:
        LOG.error(e)
        raise exceptions.APIConflict(detail=_('No available regions found'))
    if not len(regions):
        raise exceptions.APIConflict(detail=_('No available regions found'))
    # Check if requested region exists, returns the default or the first one
    region_name = request.query_params.get('region', None)
    if region_name and region_name not in [r.id for r in regions]:
        raise exceptions.APIConflict(detail='Region {} not found'.format(region_name))
    elif not region_name:
        try:
            default_region = plugin_settings.DEFAULT_REGION
        except Exception as e:
            default_region = None
            LOG.error(e)
        if default_region and default_region in [r.id for r in regions]:
            region_name = default_region
    region_name = region_name or regions.first().id
    region_options = [dict(id=r.id, description=r.description) for r in regions]
    return region_name, region_options


class RegionsViewSet(viewsets.ModelViewSet):
    permission_classes = (EndUserOnly,)
    serializer_class = RegionSerializer

    def get_queryset(self):
        return OpenstackRegion.objects.enabled_for_enduser().all()
