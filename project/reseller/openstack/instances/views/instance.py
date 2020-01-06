from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.instances.instance_status import InstanceTask
from fleio.reseller.utils import user_reseller_resources
from fleio.utils.model import statuses_dict_to_statuses_choices
from fleiostaff.openstack.instances.views import StaffInstanceViewSet


class ResellerInstanceViewSet(StaffInstanceViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        queryset = super().get_queryset().filter(
            project__service__client__reseller_resources=reseller_resources,
        ).all()

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        # TODO(manu): remove region choices once filtering in frontend is based on records search
        region_name, region_options = self.get_regions(request)
        region_filtering_options = []
        for region in region_options:
            region_filtering_options.append({
                'display': region['id'],
                'value': region['id'],
            })
        filter_options = {
            'region': region_filtering_options,
            'status': statuses_dict_to_statuses_choices(InstanceStatus.status_map.items()),
            'task_state': statuses_dict_to_statuses_choices(InstanceTask.task_state_filtering_opts_map.items())
        }
        response.data['filter_options'] = filter_options
        return response
