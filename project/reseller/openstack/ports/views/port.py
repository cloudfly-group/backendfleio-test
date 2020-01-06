import logging

from fleio.core.drf import CustomPermissions, ResellerOnly
from fleio.openstack.models import Port
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.openstack.ports.views import StaffPortViewSet

LOG = logging.getLogger(__name__)


class ResellerPortViewSet(StaffPortViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return Port.objects.filter(project__service__client__reseller_resources=reseller_resources)
