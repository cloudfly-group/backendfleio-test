from fleio.core.drf import ResellerOnly
from fleio.openstack.models import OpenstackRegion

from fleiostaff.openstack.regions.views import StaffRegionsViewSet


class ResellerRegionsViewSet(StaffRegionsViewSet):

    permission_classes = (ResellerOnly,)

    def get_queryset(self):
        return OpenstackRegion.objects.enabled_for_enduser().all()
