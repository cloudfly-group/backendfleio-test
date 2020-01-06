import copy
import logging
import threading
from typing import Optional

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from fleio.activitylog.operations import fetch_log_category
from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.conf.models import Option
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.features import staff_active_features
from fleio.openstack.models import OpenstackRegion, OpenstackRole
from fleio.openstack.serializers.regions import RegionBriefSerializer
from fleio.openstack.serializers.roles import OpenstackRoleSerializer
from fleio.openstack.settings import OSConfig
from fleio.openstack.settings import plugin_settings
from fleiostaff.openstack.settings.serializers import DefaultsSettingsSerializer
from fleiostaff.openstack.settings.serializers import NotificationsSettingsSerializer
from fleiostaff.openstack.settings.serializers import OpenstackSettingsSerializer
from fleiostaff.openstack.settings.serializers import VolumeSizeIncrementsSerializer
from .utils import connection_thread

from fleio.openstack.bin.sync import sync_openstack_objects_task
from fleio.openstack.bin.sync import sync_regions
from fleio.openstack.bin.sync import sync_roles

LOG = logging.getLogger(__name__)


def get_default_role(roles) -> Optional[str]:
    possible_default_roles = ['_member_', 'member', ]
    for possible_role in possible_default_roles:
        is_available_role = roles.filter(name=possible_role).first()
        if is_available_role:
            return is_available_role.name
    return None


def get_default_region(regions) -> Optional[str]:
    first_region = regions.first()
    return first_region.id if first_region else None


@api_view(['GET', 'POST'])
@permission_classes((StaffOnly,))
def credentials_view(request):
    conf = OSConfig(raise_if_required_not_set=False)
    if request.method == 'GET':
        serializer = OpenstackSettingsSerializer(instance=conf)
        return Response(serializer.data)
    else:
        activity_helper.start_view_activity(
            fetch_log_category('openstack'), 'openstack update credentials', request,
        )
        activity_failed = False

        try:
            if staff_active_features.is_enabled('demo'):
                raise APIBadRequest(_('Cannot change OpenStack settings in demo mode'))
            serializer = OpenstackSettingsSerializer(instance=conf, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # sync regions and role members to allow setting them in the defaults tab
            synced_regions = sync_regions()
            synced_roles = sync_roles()
            # try to set default role and region
            if not conf.default_role:
                new_default_role = get_default_role(roles=synced_roles)
                if new_default_role:
                    conf.default_role = new_default_role
                    conf.save()
            if not conf.default_region:
                new_default_region = get_default_region(regions=synced_regions)
                if new_default_region:
                    conf.default_region = new_default_region
                    conf.save()

            new_settings = OpenstackSettingsSerializer(instance=conf).data
            # also add newly found available role and region options in the response
            roles_serializer = OpenstackRoleSerializer(instance=synced_roles, many=True)
            new_settings['available_role_options'] = roles_serializer.data
            regions_serializer = RegionBriefSerializer(instance=synced_regions, many=True)
            new_settings['available_region_options'] = regions_serializer.data

            response_msg = _('Settings successfully saved. Starting sync openstack objects task.')
            sync_openstack_objects_task.delay()

            return Response({
                'detail': response_msg,
                'settings': new_settings
            }, status=HTTP_200_OK)
        except Exception:
            activity_failed = True
            raise
        finally:
            activity_helper.end_activity(failed=activity_failed)


@api_view(['GET', 'POST'])
@permission_classes((StaffOnly,))
def defaults_view(request):
    if request.method == 'GET':
        conf = OSConfig(raise_if_required_not_set=False)
        serializer = DefaultsSettingsSerializer(instance=conf)
        response_dict = serializer.data
        roles_qs = OpenstackRole.objects.all()
        roles_serializer = OpenstackRoleSerializer(instance=roles_qs, many=True)
        response_dict['available_role_options'] = roles_serializer.data
        regions_qs = OpenstackRegion.objects.all()
        regions_serializer = RegionBriefSerializer(instance=regions_qs, many=True)
        response_dict['available_region_options'] = regions_serializer.data
        return Response(response_dict)
    else:
        if staff_active_features.is_enabled('demo'):
            raise APIBadRequest(_('Cannot change OpenStack settings in demo mode'))
        conf = OSConfig(raise_if_required_not_set=False)
        serializer = DefaultsSettingsSerializer(instance=conf, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Settings saved successfully.'),
                         'defaults': serializer.data}, status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((StaffOnly,))
def notifications_view(request):
    if request.method == 'GET':
        conf = OSConfig(raise_if_required_not_set=False)
        serializer = NotificationsSettingsSerializer(instance=conf)
        return Response(serializer.data)
    else:
        if staff_active_features.is_enabled('demo'):
            raise APIBadRequest(_('Cannot change OpenStack settings in demo mode'))
        conf = OSConfig(raise_if_required_not_set=False)
        serializer = NotificationsSettingsSerializer(instance=conf, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Settings saved successfully.'),
                         'broker': serializer.data}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((StaffOnly,))
def test_notifications_connections(request):
    conf = OSConfig(raise_if_required_not_set=False)
    serializer = NotificationsSettingsSerializer(instance=conf, data=request.data)
    serializer.is_valid(raise_exception=True)
    notifications_urls = serializer.validated_data['notifications_url'] \
        if 'notifications_url' in serializer.validated_data and serializer.validated_data['notifications_url'] \
        else plugin_settings.NOTIFICATIONS_URL
    hide_password = notifications_urls == plugin_settings.NOTIFICATIONS_URL
    results = list()
    thread_list = list()
    for url in notifications_urls:
        t = threading.Thread(target=connection_thread, args=(url, results, hide_password))
        t.start()
        thread_list.append(t)

    for th in thread_list:
        th.join()

    return Response({'results': results})


@api_view(['POST'])
@permission_classes((StaffOnly,))
def test_connection(request):
    conf = OSConfig(raise_if_required_not_set=False)
    serializer = OpenstackSettingsSerializer(instance=conf, data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'detail': _('Successfully connected to OpenStack.')}, status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((StaffOnly,))
def volume_size_increments(request):
    if request.method == 'GET':
        conf = OSConfig(raise_if_required_not_set=False)
        serializer = VolumeSizeIncrementsSerializer(instance=conf)
        return Response(serializer.data)
    elif request.method == 'POST':
        conf = OSConfig(raise_if_required_not_set=False)
        serializer = VolumeSizeIncrementsSerializer(instance=conf, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Settings saved successfully.'),
                         'volume_size_increments': serializer.data.get('volume_size_increments', {})})


@api_view(['GET'])
@permission_classes((StaffOnly,))
def services(request):
    avfs = copy.deepcopy(settings.FLEIO_API_VERSIONS)
    for service in avfs:
        try:
            avfs[service]['version'] = Option.objects.get(
                section='OPENSTACK_PLUGIN',
                field='{}_api_version'.format(service.replace('-', '_'))
            ).value  # for services that contain '-' we replace it with '_' as this is how it's stored in db
        except Option.DoesNotExist:
            avfs[service]['version'] = None

    return Response({'available_service_versions': avfs})
