from common_admin.openstack.flavorgroups.views.flavor_group import AdminFlavorGroupViewSet
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import filter_queryset_for_user


@log_reseller_activity(category_name='openstack', object_name='flavor group')
class ResellerFlavorGroupViewSet(AdminFlavorGroupViewSet):
    permission_classes = (ResellerOnly, )

    def get_queryset(self):
        return filter_queryset_for_user(super().get_queryset(), self.request.user).all()
