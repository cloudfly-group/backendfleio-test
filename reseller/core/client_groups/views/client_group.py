from common_admin.core.client_groups.views.client_group import AdminClientGroupViewSet
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import filter_queryset_for_user
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.core.clientgroups.serializers import ClientGroupDetailsSerializer
from fleiostaff.core.clientgroups.serializers import ClientGroupSerializer


@log_reseller_activity(category_name='core', object_name='client group')
class ResellerClientGroupViewSet(AdminClientGroupViewSet):
    permission_classes = (ResellerOnly,)
    serializer_class = ClientGroupSerializer

    serializer_map = {
        'retrieve': ClientGroupDetailsSerializer,
    }

    def get_queryset(self):
        return filter_queryset_for_user(super().get_queryset(), self.request.user).all()

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['reseller_resources'] = user_reseller_resources(user=self.request.user)
        serializer.save()
