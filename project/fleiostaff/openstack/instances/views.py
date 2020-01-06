import crypt
import json
import logging

from django.conf import settings
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from gnocchiclient.exceptions import BadRequest
from gnocchiclient.exceptions import ClientException
from gnocchiclient.exceptions import NotFound
from keystoneauth1.exceptions import ConnectTimeout
from keystoneauth1.exceptions import EndpointNotFound
from keystoneauth1.exceptions.http import Unauthorized
from novaclient import exceptions as nova_exceptions
from novaclient.api_versions import APIVersion
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import CustomPermissions
from fleio.core.drf import StaffOnly
from fleio.core.features import staff_active_features
from fleio.core.models import Client
from fleio.core.models import Operation
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack import exceptions
from fleio.openstack import models
from fleio.openstack.api.identity import IdentityUserApi
from fleio.openstack.exceptions import APIBadRequest
from fleio.openstack.exceptions import APIConflict
from fleio.openstack.exceptions import ObjectNotFound
from fleio.openstack.exceptions import handle
from fleio.openstack.hypervisors.api import Hypervisors
from fleio.openstack.images import serializers as images_serializers
from fleio.openstack.instances.api import Instance as APIInstance
from fleio.openstack.instances.api import Instances
from fleio.openstack.instances.operations import InstanceDeletion
from fleio.openstack.instances.serializers import FlavorSerializer
from fleio.openstack.instances.serializers import FloatingIpListFilterSerializer
from fleio.openstack.instances.serializers import InstanceActionDetailsSerializer
from fleio.openstack.instances.serializers import InstanceNameSerializer
from fleio.openstack.instances.serializers import InstanceResizeSerializer
from fleio.openstack.instances.serializers import IpSerializer
from fleio.openstack.instances.serializers import MigrateSerializer
from fleio.openstack.instances.views import InstanceViewSet
from fleio.openstack.metrics import GnocchiMetrics
from fleio.openstack.models import Image, OpenstackRegion
from fleio.openstack.models import Project  # noqa
from fleio.openstack.networking.serializers import PortSerializer
from fleio.openstack.serializers.metrics import MeasuresSerializer
from fleio.openstack.settings import plugin_settings
from fleio.openstack.tasks import create_instance_from_iso_task
from fleio.openstack.tasks import create_instance_task
from fleio.openstack.tasks import create_instance_volume
from fleio.openstack.tasks import move_instance_task
from fleio.openstack.tasks import wait_for_volume_status
from fleio.openstack.utils import parse_user_data_mime
from fleio.osbackup.models import OpenStackBackupSchedule
from fleio.osbackup.serializers import BackupScheduleSerializer
from fleio.osbackup.serializers import BackupSerializer
from fleio.pkm.models import PublicKey
from fleio.pkm.serializers import PublicKeySerializer
from fleio.reseller.utils import user_reseller_resources
from fleio.utils.misc import wait_for
from fleiostaff.openstack.instances.serializers import MoveSerializer
from fleiostaff.openstack.networks.serializers import StaffNetworkSerializerExtra
from fleiostaff.openstack.signals import staff_delete_instance
from .serializers import AdminInstanceCreateSerializer
from .serializers import AdminInstanceDetailSerializer
from .serializers import AdminInstanceSerializer

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='instance',
    additional_activities={
        'move': _('Staff user {username} ({user_id}) moved instance ({object_id}).'),
    }
)
class StaffInstanceViewSet(InstanceViewSet):
    serializer_class = AdminInstanceSerializer
    permission_classes = (CustomPermissions, StaffOnly,)
    serializer_map = {'create': AdminInstanceCreateSerializer,
                      'retrieve': AdminInstanceDetailSerializer,
                      'add_floating_ip': IpSerializer,
                      'remove_floating_ip': IpSerializer,
                      'list_floating_ips': FloatingIpListFilterSerializer,
                      'migrate': MigrateSerializer,
                      'move': MoveSerializer
                      }
    search_fields = ('id', 'name', 'status', 'region', 'project__service__client__first_name',
                     'project__service__client__last_name', 'project__service__client__company', 'hostId', 'host_name')

    def user_client_filter(self):
        return Client.objects.filter(services__openstack_project__disabled=False).distinct()

    def get_instance(self, instance=None) -> APIInstance:
        instance = instance or self.get_object()
        instance_admin_api = Instances(api_session=self.identity_admin_api.session)
        return instance_admin_api.get(db_instance=instance)

    def get_session(self, instance):
        return self.identity_admin_api.session

    def get_queryset(self):
        return models.Instance.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def get_ssh_keys(self, client=None):
        if not client:
            return PublicKeySerializer(PublicKey.objects.filter(user=self.request.user), many=True).data
        ssh_keys_users = client.users.all()
        ssh_keys = PublicKeySerializer(PublicKey.objects.filter(user__in=ssh_keys_users), many=True)
        return ssh_keys.data

    @staticmethod
    def get_selected_image(project, image):
        """Validate and serialize selected image for create options"""
        if staff_active_features.is_enabled('openstack.images.shareoncreate'):
            try:
                models.Image.objects.get(pk=image.pk)
            except (models.Image.DoesNotExist, models.Image.MultipleObjectsReturned):
                raise exceptions.APIBadRequest(detail=_('Image not found'), code=404)
            return images_serializers.ImageSerializer(initial=image).to_representation(image)
        else:
            StaffInstanceViewSet.get_selected_image(project, image)

    @staticmethod
    def get_selected_volume(project, volume):
        if staff_active_features.is_enabled('openstack.images.shareoncreate'):
            try:
                models.Volume.objects.get(pk=volume.pk)
            except (models.Volume.DoesNotExist, models.Volume.MultipleObjectsReturned):
                raise exceptions.APIBadRequest(detail=_('Volume not found'), code=404)
        return StaffInstanceViewSet.get_selected_volume(project, volume)

    def get_create_options(self, client, region_name, show_in_fleio=None, requested_image=None, requested_volume=None,
                           include_community_images=False, include_shared_images=False, is_staff=True):
        return super(StaffInstanceViewSet, self).get_create_options(
            client=client,
            region_name=region_name,
            show_in_fleio=show_in_fleio,
            requested_image=requested_image,
            requested_volume=requested_volume,
            include_community_images=staff_active_features.is_enabled('openstack.images.showcommunity'),
            include_shared_images=staff_active_features.is_enabled('openstack.images.showshared'),
            is_staff=is_staff,
        )

    def perform_create(self, serializer):
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))
        project = serializer.validated_data['project']
        region = serializer.validated_data.get('region')
        nics = serializer.validated_data['nics']
        flavor = serializer.validated_data['flavor']
        user_supplied_user_data = serializer.validated_data.get('user_data', None)
        user = serializer.validated_data.get('user', 'root')
        password = serializer.validated_data.get('root_password')
        user_data_passwd_template = None
        if password:
            password = crypt.crypt(password, crypt.mksalt(
                method=getattr(settings, 'INSTANCE_PASSWORD_HASH_METHOD', crypt.METHOD_SHA512)
            ))
            if user == 'root':
                user_data_passwd_template = getattr(
                    settings, 'INSTANCE_CLOUD_INIT_ROOT_PASSWORD_SET', ''
                ).format(root_password=password)
            else:
                user_data_passwd_template = getattr(
                    settings, 'INSTANCE_CLOUD_INIT_NEW_USER_AND_PASSWORD_SET', ''
                ).format(new_user_name=user, new_user_password=password)
        ssh_keys_set_template = getattr(
            settings, 'INSTANCE_CLOUD_INIT_SSH_KEYS_SET', ''
        ).format(user=user)

        ssh_keys = serializer.validated_data.get('ssh_keys', None)

        try:
            final_user_data = parse_user_data_mime(
                user_data_passwd_template=user_data_passwd_template,
                user_supplied_user_data=user_supplied_user_data,
                ssh_keys_set_template=ssh_keys_set_template,
                keys_content=ssh_keys,
                additional_userdata=getattr(settings, 'STAFF_INSTANCE_ADDITIONAL_CLOUD_INIT_USERDATA', None),
            )
        except Exception as e:
            raise APIBadRequest(str(e))

        dev_mapping_v1 = serializer.validated_data['boot_source'].get('dev_mapping_v1')
        dev_mapping_v2 = serializer.validated_data['boot_source'].get('dev_mapping_v2')
        volume_type = serializer.validated_data['boot_source'].get('volume_type')
        boot_image = serializer.validated_data['boot_source'].get('image')
        first_boot_device = serializer.validated_data['boot_source'].get('boot_device')
        boot_image_id = boot_image.id if boot_image else None
        create_args = dict(project_id=project.project_id,
                           project_domain_id=project.project_domain_id,
                           region_name=region.id)
        user_id = self.request.user.id
        if dev_mapping_v2 and first_boot_device and volume_type:
            # NOTE(tomo): Volume type was requested, we need to create the volume first
            # since nova does not support this directly
            chain = (create_instance_volume.s(source_type=first_boot_device['source_type'],
                                              source_id=first_boot_device['uuid'],
                                              volume_type=volume_type,
                                              volume_size=first_boot_device['volume_size'],
                                              **create_args) |
                     wait_for_volume_status.s(status='available',
                                              **create_args) |
                     create_instance_task.s(name=serializer.validated_data.get('name'),
                                            image=boot_image_id,
                                            flavor=flavor.id,
                                            nics=nics,
                                            user_data=final_user_data,
                                            block_device_mapping_v2=dev_mapping_v2,
                                            block_device_mapping=dev_mapping_v1,
                                            user_id=user_id,
                                            **create_args))
            chain()
        else:
            # TODO(tomo): This create instance task is ran in sync so we can catch the exception below
            # however, we need to unify this with the above, mainly run the create async and deal with errors
            # in another way
            try:
                boot_from_iso = False
                if boot_image_id:
                    # wait for image
                    wait_for(lambda: Image.objects.filter(id=boot_image_id).count() > 0, 600)
                    boot_image_model = Image.objects.get(id=boot_image_id)
                    boot_from_iso = boot_image_model.disk_format == 'iso'

                if boot_from_iso:
                    create_instance_from_iso_task.delay(
                        volume_id=None, name=serializer.validated_data.get('name'), image=boot_image_id,
                        flavor=flavor.id, nics=nics,
                        user_data=final_user_data,
                        block_device_mapping_v2=dev_mapping_v2, block_device_mapping=dev_mapping_v1,
                        **create_args,
                    )
                else:
                    instance_id = create_instance_task(
                        volume_id=None, name=serializer.validated_data.get('name'), image=boot_image_id,
                        flavor=flavor.id, nics=nics,
                        user_data=final_user_data,
                        block_device_mapping_v2=dev_mapping_v2,
                        block_device_mapping=dev_mapping_v1, user_id=user_id, **create_args,
                    )

                    activity_helper.add_current_activity_params(object_id=instance_id)
            except Unauthorized as e:
                LOG.error(e)
                raise exceptions.OpenstackAuthError(
                    _('Project id for client does not exist, or does not have the permission for the operation'))
            except Exception as e:
                LOG.error(e)
                exceptions.handle(self.request, message=e)

    def perform_destroy(self, instance):
        instance = self.get_instance()
        try:
            instance.delete()
            Operation.objects.create(
                operation_type=InstanceDeletion.name,
                primary_object_id=instance.instance.id,
                params=json.dumps({
                    'region': instance.instance.region,
                })
            )
            user = self.request.user
            staff_delete_instance.send(sender=__name__, user=user, user_id=user.id,
                                       instance_name=instance.instance.name, instance_id=instance.uuid,
                                       username=user.username, request=self.request)
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to destroy instance %s') % instance.instance.name
            handle(self.request, message=msg)

    @action(detail=True, methods=['post'])
    def lock(self, request, id):
        instance = self.get_instance()
        try:
            instance.lock()
            # TODO: remove this when switching to versioned notifications as this will be redundant
            db_instance = instance.instance
            api_instance = instance.api_instance
            db_instance.locked = api_instance.locked
            db_instance.save()
        except Exception as e:
            exceptions.handle(request, message=e)
        return Response({'detail': _('Lock sent')})

    @action(detail=True, methods=['post'])
    def unlock(self, request, id):
        instance = self.get_instance()
        try:
            instance.unlock()
            # TODO: remove this when switching to versioned notifications as this will be redundant
            db_instance = instance.instance
            api_instance = instance.api_instance
            db_instance.locked = api_instance.locked
            db_instance.save()
        except Exception as e:
            exceptions.handle(request, message=e)
        return Response({'detail': _('Unlock sent')})

    @action(detail=True, methods=['post'])
    def suspend(self, request, id):
        instance = self.get_instance()
        try:
            instance.suspend()
        except Exception as e:
            exceptions.handle(request, message=e)
        return Response({'detail': _('Suspend sent')})

    @action(detail=True, methods=['post'])
    def resume(self, request, id):
        instance = self.get_instance()
        try:
            instance.resume()
        except Exception as e:
            exceptions.handle(request, message=e)
        return Response({'detail': _('Resume sent')})

    @action(detail=True, methods=['get'])
    def action_details(self, request, id):
        instance = self.get_instance()
        req_id = request.query_params.get('request_id', None)

        if req_id is None:
            raise exceptions.ObjectNotFound({'request_id': 'Missing required request_id parameter'})
        try:
            serializer = InstanceActionDetailsSerializer()
            data = serializer.to_representation(instance.get_action_details(req_id))
            return Response(data)
        except Exception as e:
            LOG.exception(e)
            exceptions.handle(request, message=e)

    @action(detail=True, methods=['get', 'post'])
    def resize(self, request, id):
        # TODO(tomo): Verify instance state before resize
        instance = self.get_instance()
        if request.method == 'GET':
            flavors_qs = instance.resize_flavors(staff_request=True)
            return Response({'flavors': FlavorSerializer(flavors_qs, many=True).data,
                             'instance': AdminInstanceSerializer(instance.instance).data})

        else:
            serializer = InstanceResizeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                instance.resize(flavor=serializer.validated_data['flavor'])
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to resize instance %s') % instance.instance.name
                handle(request, message=msg)
                # TODO(tomo): Update the instance details ?

        return Response({'detail': _('Instance resize started successfully')})

    @action(detail=True, methods=['get'])
    def diagnostics(self, request, id):
        instance = self.get_instance()
        data = 'Unable to get diagnostics'
        try:
            data = instance.diagnostics()[1]
        except Exception as e:
            exceptions.handle(request, message=e)
        return Response(data)

    @action(detail=True, methods=['get'])
    def add_port_options(self, request, id):
        instance = self.get_instance()
        instance_region = instance.instance.region
        networks = models.Network.objects.get_networks_for_project(project_id=instance.instance.project_id,
                                                                   external=True,
                                                                   subnet_count=True).filter(subnet_count__gt=0,
                                                                                             region=instance_region)
        if not networks:
            raise ObjectNotFound({'detail': _('No networks found for project')})
        if not hasattr(instance.instance, 'project_id'):
            raise APIConflict({'detail': _('Instance has no project')})
        return Response({'networks': StaffNetworkSerializerExtra(networks, many=True).data,
                         'project_id': instance.instance.project_id})

    @action(detail=True, methods=['get'])
    def add_ip_options(self, request, id):
        instance = self.get_instance()
        instance_region = instance.instance.region
        networks = models.Network.objects.get_networks_for_project(project_id=instance.instance.project_id,
                                                                   external=True,
                                                                   subnet_count=True).filter(subnet_count__gt=0,
                                                                                             region=instance_region)
        ports = models.Port.objects.filter(device_id=id)
        if not networks:
            raise ObjectNotFound({'detail': _('No networks found for project')})
        if not hasattr(instance.instance, 'project_id'):
            raise APIConflict({'detail': _('Instance has no project')})
        if not ports:
            raise ObjectNotFound({'detail': _('No ports found for instance')})
        return Response({'networks': StaffNetworkSerializerExtra(networks, many=True).data,
                         'ports': PortSerializer(ports, many=True).data})

    @action(detail=True, methods=['get'])
    def migrate_options(self, request, id):
        instance = self.get_instance()
        admin_session = self.identity_admin_api.session
        hypervisors = Hypervisors(api_session=admin_session).get_hypervisors(region=instance.instance.region)
        try:
            api_instance = instance.api_instance
        except nova_exceptions.NotFound:
            raise ObjectNotFound(_('Instance does not exist in OpenStack anymore.'))
        current_hypervisor = getattr(
            api_instance,
            'OS-EXT-SRV-ATTR:hypervisor_hostname',
            _('Can not get current hypervisor'),
        )
        response = {
            'current_hypervisor': current_hypervisor,
            'show_hostname_for_migrate': APIVersion(plugin_settings.compute_api_version) >= APIVersion('2.56'),
            'hypervisors': [
                {
                    'id': hv.id,
                    'name': hv.service.get('host')
                } for hv in hypervisors if hv.hypervisor_hostname != current_hypervisor
            ]
        }

        return Response(response)

    @action(detail=True, methods=['post'])
    def migrate(self, request, id):
        serializer = MigrateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_instance()
        try:
            instance.migrate(serializer.validated_data)
        except Exception as e:
            LOG.error(e)
            exceptions.handle(request, message=_('Can not migrate instance.'))
        return Response({'detail': _('Migrate in progress')})

    @action(detail=True, methods=['post'])
    def create_snapshot(self, request, id):
        create_snapshot_as_client = request.data.pop('create_snapshot_as_client', False)
        serializer = InstanceNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if create_snapshot_as_client:
            instance = self.get_object()
            try:
                project = instance.project
            except instance.project.DoesNotExist:
                raise APIBadRequest(_('Instance is not related to any project. Aborting.'))
            custom_api_session = IdentityUserApi(
                project.project_id,
                project.project_domain_id,
                cache=request.session
            ).session
            instances_api = Instances(api_session=custom_api_session)
            instance_user_api = instances_api.get(db_instance=instance)
            try:
                image_uuid = instance_user_api.create_snapshot(name=serializer.validated_data['name'])
                return Response({'image_uuid': image_uuid})
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to create snapshot for instance {0}').format(instance.name)
                handle(self.request, message=msg)
        else:
            instance = self.get_instance()
            try:
                image_uuid = instance.create_snapshot(name=serializer.validated_data['name'])
                reseller_resources = user_reseller_resources(self.request.user)
                if reseller_resources:
                    Image.objects.update_or_create(
                        defaults={
                            'reseller_resources': reseller_resources,
                            'min_disk': 0,
                            'min_ram': 0,
                            'region': OpenstackRegion.objects.get(id=instance.instance.region)
                        },
                        id=image_uuid,
                    )

                return Response({'image_uuid': image_uuid})
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to create snapshot for instance {0}').format(instance.instance.name)
                handle(self.request, message=msg)

    def check_if_can_move(self, api_instance: APIInstance, client: Client) -> bool:
        if api_instance.instance.project.service:
            if api_instance.instance.project.service.client.id == client.id:
                raise APIBadRequest(_('Instance already belongs to selected client'))

        instance_details = api_instance.api_instance.to_dict()
        hypervisor_name = instance_details.get('OS-EXT-SRV-ATTR:hypervisor_hostname')
        if super().get_instance_hypervisor_details(
            instance=api_instance,
            admin_session=self.identity_admin_api.session,
            hypervisor_name=hypervisor_name
        )['type'] in ['lxd', 'ironic']:
            raise APIBadRequest(_('Moving LXD or Ironic instances is not supported'))

        if api_instance.instance.status == 'error':
            raise APIBadRequest(_('Instance is in error state'))

        if len(api_instance.list_attached_volumes()) > 0:
            raise APIBadRequest(_('Instance has volumes attached'))

        return True

    @action(detail=True, methods=['post'])
    def move(self, request, id):
        serializer = MoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        api_instance = self.get_instance()
        try:
            # NOTE: client should and have a project since serializer checked for this
            client = Client.objects.get(id=serializer.validated_data['client'])
            project = client.first_project  # type: Project
            if self.check_if_can_move(api_instance=api_instance, client=client):
                move_instance_task.delay(
                    instance_id=api_instance.instance.id,
                    destination_project_id=project.project_id)
            else:
                raise APIBadRequest('Cannot move instance')
        except Exception as e:
            LOG.error(e)
            exceptions.handle(request, message=_('Cannot move instance.'))
        return Response({'detail': _('Move in progress')})

    @action(detail=True, methods=['post'])
    def abort_migrate(self, request, id):
        instance = self.get_instance()
        try:
            instance.abort_migrate()
        except Exception as e:
            LOG.error(e)
            exceptions.handle(request, message=_('Can not abort migrate.'))
        return Response({'detail': _('Abort migrate in progress')})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Returns a summary for instances. Used by the Dashboard widget"""
        instance_status_map_qs = self.get_queryset().values('status').annotate(count=Count('id')).order_by()
        instance_region_map = self.get_queryset().values('region').annotate(count=Count('id')).order_by()
        instance_info_avail_labels = []
        instance_info_avail_data = []
        avail_statuses = []
        instance_region_labels = [instance['region'] for instance in instance_region_map]
        instance_region_data = [instance['count'] for instance in instance_region_map]
        for instance in instance_status_map_qs:
            instance_info_avail_data.append(instance['count'])
            instance_info_avail_labels.append(instance['status'])
            avail_statuses.append(instance['status'])
        return Response({'instance_status_labels': instance_info_avail_labels,
                         'instance_status_data': instance_info_avail_data,
                         'instance_region_labels': instance_region_labels,
                         'instance_region_data': instance_region_data})

    @action(detail=True, methods=['GET'])
    def measures(self, request, id):
        """Get measures for instance."""
        instance = self.get_instance()
        ms = MeasuresSerializer(data=request.query_params)
        ms.is_valid(raise_exception=True)

        try:
            result = GnocchiMetrics(api_session=instance.api_session,
                                    region_name=instance.instance.region).get_instance_measures(instance=instance,
                                                                                                vdata=ms.validated_data)
        except BadRequest as e:
            LOG.exception('Exception when retrieving metrics: {}'.format(e))
            return Response({'measures': []})
        except NotFound as e:
            LOG.exception(e)
            return Response({'measures': []})
        except ClientException as e:
            LOG.exception(e)
            raise exceptions.APIConflict(e)
        except EndpointNotFound as e:
            LOG.exception(e)
            raise exceptions.APIConflict(e)
        except ConnectTimeout as e:
            LOG.exception(e)
            raise exceptions.APIConflict(e)

        return Response({'measures': result})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=True, methods=['get'])
    def list_security_groups(self, request, id):
        instance = self.get_instance()
        sec_gr_lists = models.Port.objects.filter(device_id=instance.instance.id).values_list('security_groups')
        sec_list = list()
        for security_group_list in sec_gr_lists:
            sec_list += [x for x in json.loads(security_group_list[0])]
        security_groups = list()
        if sec_list:
            sec_set = set(sec_list)
            sec_groups = models.SecurityGroup.objects.filter(id__in=sec_set)
            for sec_group in sec_groups:
                security_group_rules = list()
                for rule in sec_group.security_group_rules.all():
                    security_group_rules.append({'display': self._format_security_rule(rule.__dict__)})
                security_groups.append({'id': sec_group.id, 'name': sec_group.name,
                                        'description': sec_group.description,
                                        'security_group_rules': security_group_rules})
        return Response({'security_groups': security_groups})

    @action(detail=True, methods=['post'])
    def associate_security_group(self, request, id):
        try:
            group = request.data['group']
        except KeyError:
            raise exceptions.APIBadRequest(detail=_('Parameter "group" required'))

        instance = super().get_instance()
        try:
            instance.associate_security_group(group=group)
        except Exception as e:
            LOG.exception(e)
            msg = _('Unable to associate security group {group} to instance {instance_name}')
            msg = msg.format(group=group, instance_name=instance.instance.name)
            handle(self.request, message=msg)
        return Response({'detail': _('Security group associated')})

    @action(detail=True, methods=['POST'])
    def create_backup(self, request, id):
        if not staff_active_features.is_enabled('openstack.osbackup'):
            raise APIBadRequest(_('Backup feature is disabled.'))
        instance = self.get_instance()
        serializer = BackupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        backup_name = serializer.validated_data['backup_name']
        backup_type = serializer.validated_data['backup_type']
        rotation = serializer.validated_data['rotation']
        try:
            instance.compute_api.servers.backup(
                server=instance.uuid,
                backup_name=backup_name,
                backup_type=backup_type,
                rotation=rotation
            )
            return Response({
                'detail': _('Backup for instance {} was scheduled for creation').format(instance.instance.name)
            })
        except Exception as e:
            LOG.error(e)
            return Response({
                'detail': _('Unable to create backup for instance {0}').format(instance.instance.name)
            })

    @action(detail=True, methods=['GET'])
    def get_instance_backups_and_backup_schedules(self, request, id):
        if not staff_active_features.is_enabled('openstack.osbackup'):
            raise APIBadRequest(_('Backup feature is disabled.'))
        del request  # unused
        instance = self.get_instance()
        backup_schedules_qs = OpenStackBackupSchedule.objects.filter(instance__id=instance.uuid)
        backups = models.Image.objects.filter(type='backup', instance_uuid=instance.uuid)
        return Response({
            'schedules': BackupScheduleSerializer(instance=backup_schedules_qs, many=True).data,
            'backups': images_serializers.ImageBriefSerializer(instance=backups, many=True).data,
        })
