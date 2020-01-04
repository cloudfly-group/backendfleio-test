from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import StaffOnly
from fleiostaff.core.clientgroups.serializers import ClientGroupDetailsSerializer

from fleiostaff.core.clientgroups.serializers import ClientGroupSerializer

from common_admin.core.client_groups.views.client_group import AdminClientGroupViewSet


@log_staff_activity(category_name='core', object_name='client group')
class ClientGroupViewSet(AdminClientGroupViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = ClientGroupSerializer

    serializer_map = {
        'retrieve': ClientGroupDetailsSerializer,
    }
