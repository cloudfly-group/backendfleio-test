from fleio.core.drf import StaffOnly
from fleio.openstack.models import OpenstackRegion

from fleio.openstack.views.regions import RegionsViewSet


class StaffRegionsViewSet(RegionsViewSet):

    permission_classes = (StaffOnly,)

    def get_queryset(self):
        return OpenstackRegion.objects.enabled().all()
