import copy

from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from keystoneauth1.exceptions import ClientException
from keystoneauth1.exceptions import SSLError
from keystoneauth1.exceptions.connection import ConnectFailure
from keystoneauth1.exceptions.connection import ConnectTimeout

from novaclient.exceptions import ClientException as NovaClientException

from fleio.conf.exceptions import ConfigException
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import InvalidSSL, ServiceUnavailable
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.hypervisors.api import Hypervisors
from fleio.openstack.models import Image, Instance, OpenstackRegion


def update_or_create(key, count, dictionary):
    val = dictionary.get(key, None)
    if val:
        dictionary[key] = dictionary[key] + count
    else:
        dictionary[key] = count
    return dictionary


@api_view(http_method_names=['GET'])
@permission_classes((StaffOnly, ))
def operating_systems_summary_view(request):
    instance_images = Instance.objects.values('image').exclude(terminated_at__isnull=False).annotate(
        count=Count('id')).order_by()
    images = Image.objects.all()
    unknown = 0
    os_info = {}
    os_info_labels = []
    os_info_data = []
    for image in instance_images:
        try:
            db_image = images.get(id=image['image'])
            if db_image.os_distro is not None:
                os_info = update_or_create(db_image.name, image['count'], os_info)
            else:
                unknown += image['count']
        except Image.DoesNotExist:
            unknown += image['count']

    for key, value in iter(os_info.items()):
        os_info_data.append(value)
        os_info_labels.append(key)
    if unknown > 0:
        os_info_data.append(unknown)
        os_info_labels.append(_('Unknown'))
    return Response({'os_data': os_info_data, 'os_labels': os_info_labels})


@api_view(http_method_names=['GET'])
@permission_classes((StaffOnly, ))
def hypervisors_summary_view(request):
    try:
        admin_session = IdentityAdminApi(request_session=request.session).session
    except ConfigException:
        # some openstack auth setting is missing, return empty array like others from the fleio dashboard
        return Response({'hypervisors': []})
    hv = Hypervisors(api_session=admin_session)
    openstack_regions = OpenstackRegion.objects.all()
    hypervisor_data = []
    hypervisors_region_data = []
    generic_representation = [{'region': None,
                               'status': None,
                               'host_ip': None,
                               'type': None,
                               'vcpus_data': [0, 0],
                               'vcpus_labels': [_('Used vCPUs'), _('Not used vCPUs')],
                               'disk_data': [0, 0],
                               'disk_labels': [_('Used disk (GB)'), _('Free disk (GB)')],
                               'memory_data': [0, 0],
                               'memory_labels': [_('Used memory (MB)'), _('Free memory (MB)')]}]
    try:
        all_regions = copy.deepcopy(generic_representation)
        all_regions[0]['label'] = _('All Hypervisors...')
        hypervisor_data.append(all_regions)
        for region in openstack_regions:
            try:
                region_hypervisors = hv.get_hypervisors(region=region.id)
            except ConnectTimeout:
                region_hypervisors = None
            except SSLError:
                raise InvalidSSL('SSL certificate is invalid. '
                                 'Check certificate for region: {0}'.format(region))
            if region_hypervisors:
                region_data = copy.deepcopy(generic_representation)
                region_data[0]['label'] = _('All {} hypervisors').format(region)
                for hypervisor in region_hypervisors:
                    per_region = copy.deepcopy(generic_representation)
                    per_region[0]['label'] = _('Hypervisor {} - {} - {}').format(hypervisor.hypervisor_hostname,
                                                                                 hypervisor.hypervisor_type, region.id)
                    per_region[0]['region'] = region.id
                    per_region[0]['status'] = hypervisor.status
                    per_region[0]['host_ip'] = hypervisor.host_ip
                    per_region[0]['type'] = hypervisor.hypervisor_type
                    per_region[0]['vcpus_data'] = [hypervisor.vcpus_used, hypervisor.vcpus - hypervisor.vcpus_used]
                    per_region[0]['disk_data'] = [hypervisor.local_gb_used,
                                                  hypervisor.local_gb - hypervisor.local_gb_used]
                    per_region[0]['memory_data'] = [hypervisor.memory_mb_used,
                                                    hypervisor.memory_mb - hypervisor.memory_mb_used]
                    hypervisors_region_data.append(per_region)

                    region_data[0]['vcpus_data'][0] += hypervisor.vcpus_used
                    region_data[0]['vcpus_data'][1] += hypervisor.vcpus - hypervisor.vcpus_used
                    region_data[0]['disk_data'][0] += hypervisor.local_gb_used
                    region_data[0]['disk_data'][1] += hypervisor.local_gb - hypervisor.local_gb_used
                    region_data[0]['memory_data'][0] += hypervisor.memory_mb_used
                    region_data[0]['memory_data'][1] += hypervisor.memory_mb - hypervisor.memory_mb_used
                hypervisor_data[0][0]['vcpus_data'][0] += region_data[0]['vcpus_data'][0]
                hypervisor_data[0][0]['vcpus_data'][1] += region_data[0]['vcpus_data'][1]
                hypervisor_data[0][0]['disk_data'][0] += region_data[0]['disk_data'][0]
                hypervisor_data[0][0]['disk_data'][1] += region_data[0]['disk_data'][1]
                hypervisor_data[0][0]['memory_data'][0] += region_data[0]['memory_data'][0]
                hypervisor_data[0][0]['memory_data'][1] += region_data[0]['memory_data'][1]

                hypervisor_data.append(region_data)
        for region_data in hypervisors_region_data:
            hypervisor_data.append(region_data)
    except (ClientException, ConnectFailure, NovaClientException):
        raise ServiceUnavailable(_('Could not connect to openstack'))
    return Response({'hypervisors': [item for sublist in hypervisor_data for item in sublist]})
