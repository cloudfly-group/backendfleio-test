import crypt
import json
import logging
from decimal import Decimal

from django.conf import settings
from django.db.models import Case
from django.db.models import Count
from django.db.models import Q
from django.db.models import When
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from gnocchiclient.exceptions import BadRequest
from gnocchiclient.exceptions import ClientException
from gnocchiclient.exceptions import NotFound
from keystoneauth1.exceptions import ConnectTimeout
from keystoneauth1.exceptions import EndpointNotFound
from keystoneauth1.exceptions.http import Unauthorized
from novaclient.exceptions import ClientException as NovaClientException
from novaclient.exceptions import Forbidden
from novaclient.exceptions import UnsupportedConsoleType
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.billing.credit_checker import check_if_enough_credit
from fleio.billing.models import Service
from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.drf import CustomPermissions
from fleio.core.drf import EndUserOnly
from fleio.core.drf import FleioPaginationSerializer
from fleio.core.exceptions import APIConflict
from fleio.core.exceptions import ObjectNotFound
from fleio.core.features import active_features
from fleio.core.features import staff_active_features
from fleio.core.filters import CustomFilter
from fleio.core.models import Client
from fleio.core.models import Operation
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack import exceptions
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.discovery import PublicEndpoint
from fleio.openstack.hypervisors.api import Hypervisors
from fleio.openstack.images import serializers as images_serializers
from fleio.openstack.instances import serializers as instance_serializers
from fleio.openstack.instances.api import Instances
from fleio.openstack.instances.filters import InstanceFilter
from fleio.openstack.instances.filters import InstanceIpSearchFilter
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.instances.instance_status import InstanceTask
from fleio.openstack.instances.operations import InstanceDeletion
from fleio.openstack.instances.serializers import FlavorSerializer
from fleio.openstack.metrics import GnocchiMetrics
from fleio.openstack.models import Hypervisor
from fleio.openstack.models import Project
from fleio.openstack.models import VolumeSnapshot
from fleio.openstack.models import VolumeType
from fleio.openstack.models.image import OpenStackImageVisibility
from fleio.openstack.networking.serializers import FloatingIpSerializer
from fleio.openstack.networking.serializers import NetworkOptionsSerializer
from fleio.openstack.networking.serializers import NetworkSerializerExtra
from fleio.openstack.networking.serializers import PortSerializer
from fleio.openstack.osapi import OSApi
from fleio.openstack.serializers.metrics import MeasuresSerializer
from fleio.openstack.settings import plugin_settings
from fleio.openstack.signals.signals import user_delete_instance
from fleio.openstack.tasks import create_instance_from_iso_task
from fleio.openstack.tasks import create_instance_task
from fleio.openstack.tasks import create_instance_volume
from fleio.openstack.tasks import signal_boot_from_iso
from fleio.openstack.tasks import wait_for_volume_status
from fleio.openstack.utils import OSAuthCache
from fleio.openstack.utils import parse_user_data_mime
from fleio.osbackup.models import OpenStackBackupSchedule
from fleio.osbackup.serializers import BackupScheduleSerializer
from fleio.osbackup.serializers import BackupSerializer
from fleio.osbilling.models import TIME_UNIT_MAP
from fleio.osbilling.models import VALUE_UNIT_MAP
from fleio.osbilling.price_calculator.monetary_amount import MonetaryAmount
from fleio.osbilling.price_calculator.rule_price_calculator import RulePriceCalculator
from fleio.pkm.models import PublicKey
from fleio.pkm.serializers import PublicKeySerializer
from fleio.utils.misc import wait_for
from fleio.utils.model import statuses_dict_to_statuses_choices
from ..exceptions import APIBadRequest
from ..exceptions import OpenstackAuthError
from ..exceptions import handle
from ..models import FloatingIp
from ..models import Image
from ..models import Instance as InstanceModel
from ..models import Network
from ..models import OpenstackInstanceFlavor
from ..models import OpenstackRegion
from ..models import Port
from ..models import SecurityGroup
from ..models import Volume as VolumeModel

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='openstack', object_name='instance',
)
class InstanceViewSet(viewsets.ModelViewSet):
    serializer_class = instance_serializers.InstanceSerializer
    serializer_map = {'create': instance_serializers.InstanceCreateSerializer,
                      'retrieve': instance_serializers.InstanceDetailSerializer,
                      'add_floating_ip': instance_serializers.AddFloatingIpSerializer,
                      'remove_floating_ip': instance_serializers.AddFloatingIpSerializer,
                      'list_floating_ips': instance_serializers.FloatingIpListFilterSerializer,
                      'create_backup': BackupSerializer,
                      }
    http_method_names = ['get', 'post', 'options', 'delete', 'head']
    permission_classes = (EndUserOnly, CustomPermissions)
    filter_backends = (filters.OrderingFilter, InstanceIpSearchFilter, CustomFilter, DjangoFilterBackend)
    filter_class = InstanceFilter
    search_fields = ('name', 'id')
    # TODO: use another name for lookup field since it conflicts with internal name
    lookup_field = 'id'
    ordering_fields = ('name', 'region', 'status', 'created', 'current_cycle_traffic', 'current_month_traffic')
    pagination_class = FleioPaginationSerializer

    def get_queryset(self):
        user_clients = self.request.user.clients.all()
        user_services = Service.objects.filter(openstack_project__isnull=False, client__in=user_clients).distinct()
        return InstanceModel.objects.filter(project__service__in=user_services)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def user_client_filter(self):
        """Get all clients the current user has access to"""
        return self.request.user.clients.filter(services__openstack_project__disabled=False).distinct()

    def get_request_user_client(self, client_id=None):
        """
        Retrieve the request user client with the specified id or return the
        first one with an OpenStack project.
        """
        if client_id is None:
            client = self.user_client_filter().first()
        else:
            try:
                client = self.user_client_filter().get(id=client_id)
            except Client.DoesNotExist as e:
                LOG.error(e)
                raise exceptions.APIBadRequest(detail=_('Client not found'))
            except Exception as e:
                LOG.exception(e)
                raise exceptions.APIBadRequest(detail=_('Client not available'))
        if client is None:  # NOTE(tomo): If client_id not provided, client can be none
            raise exceptions.APIConflict(detail=_('No client with an enabled OpenStack project found'))
        return client

    def os_api(self, project_id, domain_id, cache=True):
        """Create an OSApi instance with cache in session from a request"""
        if cache:
            auth_cache = OSAuthCache(request_session=self.request.session)
        else:
            auth_cache = None
        return OSApi(project=project_id,
                     domain=domain_id,
                     auth_cache=auth_cache)

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def get_session(self, instance):
        client_session = self.os_api(
            project_id=instance.project.project_id,
            domain_id=instance.project.project_domain_id,
        ).get_session()
        return client_session

    def get_instance(self):
        """
        Create an Instance class to combine both API and DB objects.
        This uses the get_queryset method to filter for the permitted resources.
        The os_api created is based on the Instance project, assuming the user has access
        to the client associated with that project (determined from the get_queryset above).
        :rtype: .instance.Instance
        """
        instance = self.get_object()
        return self.os_api(
            project_id=instance.project.project_id,
            domain_id=instance.project.project_domain_id,
        ).instances.get(instance)

    def get_admin_instance(self, instance=None):
        instance = instance or self.get_object()
        instance_admin_api = Instances(api_session=self.identity_admin_api.session)
        return instance_admin_api.get(db_instance=instance)

    @staticmethod
    def get_project_images(
            project_id,
            region_id,
            status='active',
            include_community_images: bool = False,
            include_shared_images: bool = False,
            filter_args=None,
            exclude_args=None,
            filter_against_flavor=None,
            client=None,
    ):
        # Get all project images
        project_images = Image.objects.get_images_for_project(project_id=project_id).filter(
            region_id=region_id,
            status=status
        )  # This actually gets all images that a project can see (meaning same project images + shared + community...)

        assigned_to_flavor_or_group = []
        if filter_against_flavor:
            assigned_to_flavor_or_group = project_images.filter(
                Q(flavors__in=[filter_against_flavor, ]) | Q(flavor_groups__in=[filter_against_flavor.flavor_group, ])
            )

        if filter_args:
            project_images = project_images.filter(**filter_args)

        if exclude_args:
            project_images = project_images.exclude(**exclude_args)

        owned_images = []
        public_images = []
        shared_images = []
        community_images = []
        for image in project_images:
            if filter_against_flavor:
                # add info about whether the image is assigned to the selected flavor or flavor's group
                if (image not in assigned_to_flavor_or_group and
                        not (image.flavors.count() == 0 and image.flavor_groups.count() == 0)):
                    image.assigned_to_flavor = False
            if image.project_id == project_id:
                owned_images.append(image)
            elif image.visibility == OpenStackImageVisibility.PUBLIC and image.project_id != project_id:
                if client:
                    if image.reseller_resources == client.reseller_resources:
                        public_images.append(image)
                else:
                    public_images.append(image)
            elif (include_shared_images and image.visibility == OpenStackImageVisibility.SHARED and
                  image.project_id != project_id):
                for member in image.members.all():
                    if member.status == 'accepted':
                        shared_images.append(image)
            elif (include_community_images and image.visibility == OpenStackImageVisibility.COMMUNITY and
                  image.project_id != project_id):
                if client:
                    if image.reseller_resources == client.reseller_resources:
                        community_images.append(image)
                else:
                    community_images.append(image)

        o_images = images_serializers.ImageSerializer(owned_images, many=True)
        p_images = images_serializers.ImageSerializer(public_images, many=True)
        s_images = images_serializers.ImageSerializer(shared_images, many=True)
        c_images = images_serializers.ImageSerializer(community_images, many=True)
        return p_images.data, o_images.data, s_images.data, c_images.data

    def perform_create(self, serializer):
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Failed to create instance, please contact support'))
        nics = serializer.validated_data.pop('nics', None)
        project = serializer.validated_data['project']
        region = serializer.validated_data.get('region')
        flavor = serializer.validated_data.get('flavor')
        if flavor and flavor.out_of_stock:
            raise exceptions.ForbiddenException('Cannot create instance using out of stock flavor.')
        user_supplied_user_data = serializer.validated_data.get('user_data')
        dev_mapping_v1 = serializer.validated_data['boot_source'].get('dev_mapping_v1')
        dev_mapping_v2 = serializer.validated_data['boot_source'].get('dev_mapping_v2')
        volume_type = serializer.validated_data['boot_source'].get('volume_type')
        boot_image = serializer.validated_data['boot_source'].get('image')
        first_boot_device = serializer.validated_data['boot_source'].get('boot_device')
        boot_image_id = boot_image.id if boot_image else None
        create_args = dict(project_id=project.project_id,
                           project_domain_id=project.project_domain_id,
                           region_name=region.id)

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
        ssh_keys_set_template = getattr(settings, 'INSTANCE_CLOUD_INIT_SSH_KEYS_SET', '').format(user=user)

        ssh_keys = serializer.validated_data.get('ssh_keys', None)

        try:
            final_user_data = parse_user_data_mime(
                user_data_passwd_template=user_data_passwd_template,
                user_supplied_user_data=user_supplied_user_data,
                ssh_keys_set_template=ssh_keys_set_template,
                keys_content=ssh_keys,
                additional_userdata=getattr(settings, 'ENDUSER_INSTANCE_ADDITIONAL_CLOUD_INIT_USERDATA', None),
            )
        except Exception as e:
            raise APIBadRequest(str(e))

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
                # wait for image
                if boot_image_id:
                    wait_for(lambda: Image.objects.filter(id=boot_image_id).count() > 0, 600)
                    boot_image_model = Image.objects.get(id=boot_image_id)
                    boot_from_iso = boot_image_model.disk_format == 'iso'
                else:
                    boot_from_iso = False
                if boot_from_iso:
                    create_instance_from_iso_task.delay(
                        volume_id=None, name=serializer.validated_data.get('name'), image=boot_image_id,
                        flavor=flavor.id, nics=nics, user_data=final_user_data, block_device_mapping_v2=dev_mapping_v2,
                        block_device_mapping=dev_mapping_v1,
                        **create_args,
                    )
                else:
                    instance_id = create_instance_task(
                        volume_id=None,
                        name=serializer.validated_data.get('name'),
                        image=boot_image_id,
                        flavor=flavor.id,
                        nics=nics,
                        user_data=final_user_data,
                        block_device_mapping_v2=dev_mapping_v2,
                        block_device_mapping=dev_mapping_v1,
                        user_id=user_id,
                        **create_args
                    )

                    activity_helper.add_current_activity_params(object_id=instance_id)
            except Unauthorized as e:
                # TODO(tomo): this exception is no longer valid here since we use celery tasks
                LOG.error(e)
                raise exceptions.OpenstackAuthError(_('Permission denied'))
            except Forbidden as e:
                # TODO(tomo): this exception is no longer valid here since we use celery tasks
                e_msg = force_text(e)
                if e_msg.startswith('Quota exceeded'):
                    raise exceptions.ForbiddenException(detail='Cannot create instance since it would exceed quota')
                else:
                    LOG.error(e)
                    handle(self.request, message=_('Unable to create the instance'))
            except NovaClientException as e:
                # TODO(tomo): this exception is no longer valid here since we use celery tasks
                LOG.error(e)
                handle(self.request, message=_('Unable to create the instance'))

    def perform_destroy(self, instance):
        instance = self.get_instance()
        if instance.instance.locked:
            raise APIBadRequest(detail=_('Cannot delete a locked instance'))

        try:
            instance.delete()
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to destroy instance %s') % instance.instance.name
            handle(self.request, message=msg)
        else:
            Operation.objects.create(
                operation_type=InstanceDeletion.name,
                primary_object_id=instance.instance.id,
                params=json.dumps({
                    'region': instance.instance.region,
                })
            )
            user = self.request.user
            user_delete_instance.send(sender=__name__, user=user, user_id=user.id,
                                      instance_name=instance.instance.name, instance_id=instance.uuid,
                                      username=user.username, request=self.request)

    def get_ssh_keys(self, client=None):
        """Gets ssh keys for the currently logged user"""
        user_id = self.request.user.id
        ssh_keys = PublicKeySerializer(PublicKey.objects.filter(user__id=user_id), many=True)
        return ssh_keys.data

    @staticmethod
    def get_volume_size_increment(size_increments, volume_type, region):
        if type(size_increments) is dict:
            volume_size_increments_in_region = size_increments.get(region, [])
        else:
            volume_size_increments_in_region = {}
        size_increment = volume_size_increments_in_region.get(volume_type, 1)
        try:
            size_increment = int(size_increment)
        except (ValueError, TypeError):
            size_increment = 1
        return size_increment

    @staticmethod
    def get_selected_image(project, image):
        """Validate and serialize selected image for create options"""
        try:
            Image.objects.get_images_for_project(project_id=project.project_id).get(pk=image.pk)
        except (Image.DoesNotExist, Image.MultipleObjectsReturned):
            raise exceptions.APIBadRequest(detail=_('Image not found'), code=404)
        else:
            return images_serializers.ImageSerializer(initial=image).to_representation(image)

    @staticmethod
    def get_selected_volume(project, volume):
        """Validate and get serialized version of volume"""
        try:
            vol_ser = VolumeModel.objects.get(pk=volume.pk, project=project).values('id',
                                                                                    'name',
                                                                                    'description',
                                                                                    'region',
                                                                                    'size',
                                                                                    'type',
                                                                                    'created_at')
        except (VolumeModel.DoesNotExist, VolumeModel.MultipleObjectsReturned):
            raise exceptions.APIBadRequest(detail=_('Volume not found'), code=404)
        else:
            if not volume.bootable:
                raise exceptions.APIBadRequest(detail=_('Volume is not bootable'))
            if volume.status != 'available':
                raise exceptions.APIBadRequest(detail=_('Volume status must be available'))
            return vol_ser  # Already a dict

    def get_create_options(self, client, region_name, show_in_fleio=True, requested_image=None,
                           requested_volume=None, include_community_images=False, include_shared_images=False,
                           is_staff=False):
        """Instance create options based on region and client."""
        # Get the first project from the Client doing the request
        project_id = client.first_project.project_id

        include_community_images = (include_community_images if is_staff is True else
                                    active_features.is_enabled('openstack.images.showcommunity'))
        include_shared_images = (include_shared_images if is_staff is True else
                                 active_features.is_enabled('openstack.images.showshared'))
        # Get all available images
        p_images, o_images, s_images, c_images = self.get_project_images(
            project_id=project_id,
            region_id=region_name,
            include_community_images=include_community_images,
            include_shared_images=include_shared_images,
            client=client,
        )

        # Select flavors
        flavors_query = OpenstackInstanceFlavor.objects.get_for_project(
            project_id=project_id,
            disabled=False,
            region=region_name,
            deleted=False,
            is_public=True,
            show_in_fleio=show_in_fleio,
        )

        if client.reseller_resources:
            flavors_query = flavors_query.filter(
                Q(reseller_resources=client.reseller_resources) |
                Q(used_by_resellers=client.reseller_resources)
            )

        flavors = instance_serializers.FlavorSerializer(flavors_query.order_by('memory_mb'), many=True)
        ssh_keys = self.get_ssh_keys(client=client)

        # Select networks
        networks = Network.objects.get_networks_for_project(
            project_id=project_id,
            subnet_count=True
        ).filter(
            subnet_count__gt=0,
            region=region_name
        ).annotate(
            relevancy=Count(Case(When(network_tags__tag_name='public', then=1)))  # order networks by 'public' tag
        ).order_by('-relevancy')

        nics = NetworkOptionsSerializer(instance=networks, many=True)

        if is_staff:
            region = OpenstackRegion.objects.enabled().filter(
                id=region_name
            ).first()  # type: OpenstackRegion
        else:
            region = OpenstackRegion.objects.enabled_for_enduser().filter(
                id=region_name
            ).first()  # type: OpenstackRegion

        # Volumes and volume types with size increments
        volume_boot_feature = region.enable_volumes
        if is_staff:
            volume_boot_feature = volume_boot_feature and (
                staff_active_features.is_enabled('openstack.volumes') and
                staff_active_features.is_enabled('openstack.volumes.boot')
            )
        else:
            volume_boot_feature = volume_boot_feature and (
                active_features.is_enabled('openstack.volumes') and
                active_features.is_enabled('openstack.volumes.boot')
            )
        if volume_boot_feature:
            available_volumes = VolumeModel.objects.filter(
                project__project_id=project_id,
                status='available',
                bootable=True,
                region=region_name
            ).values('id', 'name', 'description', 'region', 'size', 'type', 'created_at')
            available_volume_snapshots = VolumeSnapshot.objects.filter(
                project__project_id=project_id,
                status='available',
                region=region_name
            ).values('id', 'name', 'description', 'region', 'size', 'created_at')
            size_inc = plugin_settings.volume_size_increments
            for av_vol in available_volumes:
                if av_vol.get('type'):
                    db_vol_type = VolumeType.objects.filter(region=region_name, name=av_vol['type']).first()
                    if db_vol_type and db_vol_type.description:
                        av_vol['type_display'] = db_vol_type.description
                    else:
                        av_vol['type_display'] = db_vol_type.name
                    av_vol['sizeIncrement'] = self.get_volume_size_increment(size_increments=size_inc,
                                                                             volume_type=av_vol.get('type'),
                                                                             region=region_name)
            # Get volume types
            volume_types = []
            for volume_type in VolumeType.objects.public().filter(region=region_name):
                volume_types.append({'name': volume_type.name,
                                     'description': volume_type.description or volume_type.name,
                                     'sizeIncrement': self.get_volume_size_increment(size_increments=size_inc,
                                                                                     volume_type=volume_type.name,
                                                                                     region=region_name)})
        else:
            available_volumes = []
            volume_types = []
            available_volume_snapshots = []

        create_options = {
            'bootSources': {
                'image': p_images,
                'owned_image': o_images,
                'shared_image': s_images,
                'community_image': c_images,
                'volume': available_volumes,
                'volume_snapshot': available_volume_snapshots,
                'volume_types': volume_types,
                'requested_boot_source': False,
            },
            'flavor': flavors.data,
            'ssh_key': ssh_keys,
            'nics': nics.data,
            'enable_volumes': volume_boot_feature,
            'enable_snapshots': region.enable_snapshots,
        }

        if requested_image:
            serialized_requested_image = self.get_selected_image(project=client.first_project,
                                                                 image=requested_image)
            image_min_disk = serialized_requested_image['min_disk']
            image_min_ram = serialized_requested_image['min_ram']
            filtered_flavors = []

            flavors = self.get_flavors_for_image(client, requested_image, is_staff)

            for flavor in flavors:
                if flavor['root_gb'] >= image_min_disk and flavor['memory_mb'] >= image_min_ram:
                    filtered_flavors.append(flavor)

            create_options['flavor'] = filtered_flavors
            create_options['bootSources']['requested_image'] = [serialized_requested_image]
            create_options['bootSources']['requested_boot_source'] = True
        elif requested_volume:
            serialized_requested_volume = self.get_selected_volume(project=client.first_project,
                                                                   volume=requested_volume)
            create_options['bootSources']['requested_volume'] = [serialized_requested_volume]
            create_options['bootSources']['requested_boot_source'] = True

        if not is_staff:
            create_options['can_create_resource'] = check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            )

        return create_options

    @staticmethod
    def get_regions(request: Request):
        try:
            if request.user.is_staff:
                regions = OpenstackRegion.objects.enabled().all()
            else:
                regions = OpenstackRegion.objects.enabled_for_enduser().all()
        except Exception as e:
            LOG.error(e)
            raise exceptions.APIConflict(detail='Unable to get the available regions')
        if not len(regions):
            raise exceptions.APIConflict(detail='No available regions found')
        # Check if requested region exists, returns the default or the first one
        region_name = request.query_params.get('region', None)
        if region_name and region_name not in [r.id for r in regions]:
            raise exceptions.APIConflict(detail='Region {} not found'.format(region_name))
        elif not region_name:
            try:
                default_region = plugin_settings.DEFAULT_REGION
            except Exception as e:
                default_region = None
                LOG.error(e)
            if default_region and default_region in [r.id for r in regions]:
                region_name = default_region
        region_name = region_name or regions.first().id
        region_options = [dict(id=r.id, description=r.description) for r in regions]
        return region_name, region_options

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        del args, kwargs  # unused
        client_id = self.request.query_params.get('client')
        region_requested = request.query_params.get('region', None) is not None  # If specific region is requested
        image_id = request.query_params.get('image')
        volume_id = request.query_params.get('volume')

        client = self.get_request_user_client(client_id=client_id)
        region_name, region_options = self.get_regions(request)

        # Validate only one of image_id or volume_id is specified
        if image_id and volume_id:
            raise exceptions.APIBadRequest(_('Request an image or a volume, not both'))
        # Get the image and volume model and validate further
        requested_image = requested_volume = None
        if image_id:
            try:
                requested_image = Image.objects.get(pk=image_id)
            except (Image.DoesNotExist, Image.MultipleObjectsReturned, ValueError, TypeError):
                raise exceptions.APIBadRequest(detail=_('Invalid image requested'))
        elif volume_id:
            try:
                requested_volume = VolumeModel.objects.filter(pk=volume_id).first()
            except (VolumeModel.DoesNotExist, VolumeModel.MultipleObjectsReturned, ValueError, TypeError):
                raise exceptions.APIBadRequest(detail=_('Invalid volume requested'))

        if requested_image and requested_image.region_id != region_name:
            if region_requested:
                # If the region was requested together with the image from another region, raise
                raise exceptions.APIBadRequest(_('Image not available in region {}').format(region_name))
            else:
                # otherwise set the region_name to the same region as the image
                region_name = requested_image.region_id
        elif requested_volume and requested_volume.region != region_name:
            # Do the same as above for images
            if region_requested:
                raise exceptions.APIBadRequest(_('Volume not available in region {}').format(region_name))
            else:
                region_name = requested_volume.region

        create_options = self.get_create_options(client=client,
                                                 region_name=region_name,
                                                 requested_image=requested_image,
                                                 requested_volume=requested_volume)
        create_options['region'] = region_options
        create_options['selected_region'] = region_name
        create_options['client'] = ClientMinSerializer(client).data
        return Response(create_options)

    @action(detail=False, methods=['get'])
    def get_flavors_assigned_to_image(self, request):
        try:
            image = Image.objects.get(id=request.query_params.get('image_id', None))
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))

        user = request.user
        if not user.is_staff:
            client = user.clients.first()
        else:
            selected_client_id = request.query_params.get('selected_client_id', None)
            if not selected_client_id:
                raise APIBadRequest(_('Select a client'))
            client = Client.objects.filter(id=selected_client_id).first()
        is_staff = user.is_staff

        flavors = self.get_flavors_for_image(client, image, is_staff)

        return Response(
            {
                'flavors': flavors
            }
        )

    @staticmethod
    def get_flavors_for_image(client, image, is_staff):
        generic_filter_params = dict(
            region=image.region, is_public=True,
        )
        if not is_staff:
            generic_filter_params['show_in_fleio'] = True
        if image.flavors.count() + image.flavor_groups.count() == 0:
            flavors = FlavorSerializer(
                OpenstackInstanceFlavor.objects.get_for_client(client=client).filter(
                    **generic_filter_params
                ).order_by('memory_mb'),
                many=True,
            ).data
        else:
            flavors_queryset = OpenstackInstanceFlavor.objects.get_for_client(client=client).filter(
                Q(images__id=image.id) |
                Q(flavor_group__images__id=image.id)
            ).filter(**generic_filter_params)

            flavors = FlavorSerializer(flavors_queryset.order_by('memory_mb'), many=True).data
        return flavors

    @action(detail=False, methods=['get'])
    def get_images_assigned_to_flavors_or_flavor_group(self, request):
        region = request.query_params.get('region', None)
        if not region:
            raise APIBadRequest(_('No region to filter against'))
        selected_flavor_id = request.query_params.get('selected_flavor_id', None)
        images_assigned_exists = False
        flavor = None
        if selected_flavor_id:
            flavor = OpenstackInstanceFlavor.objects.filter(id=selected_flavor_id).first()
            if not flavor:
                raise APIBadRequest(_('No flavor to filter against'))
            images_assigned_exists = Image.objects.filter(
                Q(flavors__in=[flavor, ]) | Q(flavor_groups__in=[flavor.flavor_group, ])
            ).count() > 0
        if request.user.is_staff:
            client = Client.objects.filter(id=request.query_params.get('selected_client_id', None)).first()
            if not client or not client.first_project:
                # TODO: client selection on instance create should be optional thus this has to be removed
                # and all images used (regardless of project)
                raise APIBadRequest(_('You need to select a client'))
        else:
            client = request.user.clients.first()
        include_community_images = active_features.is_enabled('openstack.images.showcommunity')
        include_shared_images = active_features.is_enabled('openstack.images.showshared')
        try:
            project_id = client.first_project.project_id
        except (Exception, AttributeError):
            raise APIBadRequest(_('Related client has no project'))

        p_images, o_images, s_images, c_images = self.get_project_images(
            project_id=project_id,
            region_id=region,
            include_community_images=include_community_images,
            include_shared_images=include_shared_images,
            filter_against_flavor=flavor if images_assigned_exists else None,
            client=client,
        )
        return Response({
            'bootSources': {
                'image': p_images,
                'owned_image': o_images,
                'shared_image': s_images,
                'community_image': c_images,
            }})

    @action(detail=False, methods=['get'])
    def filter_options(self, request, *args, **kwargs):
        del args, kwargs  # unused
        region_name, region_options = self.get_regions(request)
        filter_options = {
            'region': region_options,
            'statuses': statuses_dict_to_statuses_choices(InstanceStatus.status_map.items()),
            'task_states': statuses_dict_to_statuses_choices(InstanceTask.task_state_filtering_opts_map.items())
        }
        return Response(filter_options)

    @action(detail=True, methods=['post'])
    def start(self, request, id):
        instance = self.get_instance()
        try:
            instance.start()
        except Unauthorized as e:
            LOG.error(e)
            raise OpenstackAuthError(_('Project id not found or suspended or does not have the permission '
                                       'for the operation.'))
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to start the instance %s') % instance.instance.name
            handle(request, message=msg)
        return Response({'detail': _('Instance is starting')})

    @action(detail=True, methods=['post'])
    def stop(self, request, id):
        instance = self.get_instance()
        try:
            instance.stop()
        except Unauthorized as e:
            LOG.error(e)
            raise OpenstackAuthError(_('Project id not found or suspended or does not have the permission '
                                       'for the operation.'))
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to stop instance %s') % instance.instance.name
            handle(request, message=msg)
        return Response({'detail': _('Instance is stopping')})

    @action(detail=True, methods=['get', 'post'])
    def rebuild(self, request, id):
        instance = self.get_instance()
        client = Client.objects.filter(
            services__openstack_project__project_id=instance.instance.project.project_id
        ).first()
        if request.method == 'GET':
            p_images, o_images, s_images, c_images = self.get_project_images(
                instance.instance.project_id,
                instance.instance.region,
                exclude_args={'disk_format': 'iso'},
                client=client,
            )
            inst_serialized = instance_serializers.InstanceSerializer().to_representation(instance=instance.instance)
            ssh_keys = self.get_ssh_keys(client=client)
            return Response({
                'bootSources': {
                    'image': p_images,
                    'owned_image': o_images,
                    'shared_image': s_images
                },
                'instance': inst_serialized,
                'ssh_keys': ssh_keys,
            })
        elif request.method == 'POST':
            rebuild_data = request.data
            if client:
                rebuild_data['client_id'] = client.id
            serializer = instance_serializers.InstanceRebuildSerializer(data=rebuild_data)
            serializer.is_valid(raise_exception=True)

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
            ssh_keys_dict = serializer.validated_data.get('ssh_keys', None)

            try:
                final_user_data = parse_user_data_mime(
                    user_data_passwd_template=user_data_passwd_template,
                    user_supplied_user_data=user_supplied_user_data,
                    ssh_keys_set_template=ssh_keys_set_template,
                    keys_content=ssh_keys_dict,
                    additional_userdata=getattr(settings, 'INSTANCE_REBUILD_ADDITIONAL_USER_DATA', None),
                )
            except Exception as e:
                raise APIBadRequest(str(e))

            try:
                instance.rebuild(
                    instance_id=id,
                    image_id=serializer.validated_data.get('image'),
                    name=serializer.validated_data.get('name'),
                    userdata=final_user_data,
                )
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to rebuild the instance {}').format(instance.instance.name)
                handle(request, message=msg)
            return Response({'detail': _('Instance rebuild started successfully')})
        else:
            return Response({'detail': _('Invalid request')}, status=400)

    @action(detail=True, methods=['get', 'post'])
    def rescue(self, request, id):
        instance = self.get_instance()
        if instance.status not in [InstanceStatus.ACTIVE, InstanceStatus.STOPPED]:
            raise APIBadRequest(_('Instance must be RUNNING or STOPPED in order to rescue'))

        if request.method == 'GET':
            try:
                client = instance.instance.project.service.client
            except Exception as e:
                del e  # unused
                client = None
            p_images, o_images, s_images, c_images = self.get_project_images(
                instance.instance.project_id,
                instance.instance.region,
                exclude_args={'disk_format': 'iso'},
                client=client,
            )
            return Response({'image': {'pub': p_images, 'own': o_images, 'shr': s_images},
                             'instance': instance_serializers.InstanceSerializer(instance.instance).data
                             })
        elif request.method == 'POST':
            serializer = instance_serializers.InstanceRescueSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                instance.instance.booted_from_iso = False
                instance.instance.save()
                instance.rescue(image=serializer.validated_data['image'],
                                password=serializer.validated_data.get('root_password', None))
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to rescue instance %s') % instance.instance.name
                handle(request, message=msg)
                # TODO(tomo): Update the instance details ?
        return Response({'detail': _('Instance rescue started successfully')})

    @action(detail=True, methods=['get', 'post'])
    def boot_from_iso(self, request, id):
        instance = self.get_instance()
        if instance.status not in [InstanceStatus.ACTIVE, InstanceStatus.STOPPED]:
            raise APIBadRequest(_('Instance must be RUNNING or STOPPED in order to boot from ISO'))

        if request.method == 'GET':
            try:
                client = instance.instance.project.service.client
            except Exception as e:
                del e  # unused
                client = None
            p_images, o_images, s_images, c_images = self.get_project_images(
                instance.instance.project_id,
                instance.instance.region,
                filter_args={'disk_format': 'iso'},
                client=client,
            )
            return Response({'image': {'pub': p_images, 'own': o_images, 'shr': s_images},
                             'instance': instance_serializers.InstanceSerializer(instance.instance).data
                             })
        elif request.method == 'POST':
            serializer = instance_serializers.InstanceBootFromIsoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                instance.instance.booted_from_iso = True
                instance.instance.save()
                instance.rescue(image=serializer.validated_data['image'])
                signal_boot_from_iso.delay(instance_id=instance.instance.id)
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to boot instance %s from ISO') % instance.instance.name
                handle(request, message=msg)
            return Response({'detail': _('Instance boot form ISO started successfully')})

    @action(detail=True, methods=['post'])
    def unrescue(self, request, id):
        instance = self.get_instance()
        try:
            instance.unrescue()
        except Exception as e:
            LOG.error(e)
            msg = _('Unable exit rescue mode for instance {0}').format(instance.instance.name)
            handle(request, message=msg)
        return Response({'detail': _('Leaving rescue mode')})

    @action(detail=True, methods=['post'])
    def confirm_resize(self, request, id):
        instance = self.get_instance()
        try:
            instance.confirm_resize()
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to confirm the resize of instance {0}').format(instance.instance.name)
            handle(request, message=msg)
        return Response({'detail': _('Resize confirmed')})

    @action(detail=True, methods=['post'])
    def revert_resize(self, request, id):
        instance = self.get_instance()
        try:
            instance.revert_resize()
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to revert the resize of instance {0}').format(instance.instance.name)
            handle(request, message=msg)
        return Response({'detail': _('Reverting size')})

    @action(detail=True, methods=['get', 'post'])
    def resize(self, request, id):
        # TODO(tomo): Verify instance state before resize
        instance = self.get_instance()
        if request.method == 'GET':
            flavors_qs = instance.resize_flavors()
            return Response({'flavors': instance_serializers.FlavorSerializer(flavors_qs, many=True).data,
                             'instance': instance_serializers.InstanceSerializer(instance.instance).data})

        else:
            serializer = instance_serializers.InstanceResizeSerializer(data=request.data)
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
    def get_console_output(self, request, id):
        serializer = instance_serializers.SysLogLengthSerializer(data=request.GET)
        instance = self.get_instance()
        length = 30
        if serializer.is_valid():
            length = serializer.data['length']

        try:
            console_output = instance.system_log(length=length)
        except Exception as e:
            LOG.error(e)
            console_output = _('Unable to retrieve system log for instance {0}').format(instance.instance.name)
        return Response({'console_text': console_output, 'length': length})

    def get_lxc_console_url(
            self,
            compute_node,
            compute_node_ip,
            instance_internal_name,
            instance_id,
            tenant_id,
    ):
        url_template = \
            'lxc/lxc.html?compute_node={compute_node}&endpoint={endpoint}&id={id}' \
            '&uuid={uuid}&tenant_id={tenant_id}&auth={auth}'
        instance = self.get_object()
        client_session = self.get_session(instance)
        # attempt to fetch endpoint from openstack
        endpoint = None
        try:
            proxy_service_type = settings.LXC_CONSOLE_PROXY_SERVICE_TYPE
            if proxy_service_type:
                lxc_endpoint = PublicEndpoint(api_session=client_session, service_type=proxy_service_type)
                endpoint = lxc_endpoint.unvalidated_endpoint_url(region=instance.region)
                if endpoint:
                    endpoint = endpoint.replace('http://', 'ws://')
        except Exception as e:
            del e  # unused
            LOG.exception(
                'Exception when retrieving lxc console proxy endpoint for region {}'.format(
                    instance.region,
                )
            )
        if not endpoint:
            # use compute node as endpoint
            console_port = settings.LXC_CONSOLE_PROXY_PORT
            endpoint = 'ws://{}:{}'.format(compute_node_ip, console_port)
        return url_template.format(
            compute_node=compute_node,
            endpoint=endpoint,
            id=instance_internal_name,
            uuid=instance_id,
            tenant_id=tenant_id,
            auth=client_session.auth.get_access(client_session).auth_token,
        )

    @staticmethod
    def get_instance_hypervisor_details(instance, admin_session, hypervisor_name) -> dict:
        # first lookup in database
        db_hypervisors = Hypervisor.objects.filter(host_name=instance.instance.host_name)
        if db_hypervisors.count() == 1:
            db_hypervisor = db_hypervisors.first()  # type: Hypervisor
            if db_hypervisor.hypervisor_type:
                return {
                    'type': db_hypervisor.hypervisor_type,
                    'ip': db_hypervisor.host_ip
                }

        # hypervisor type not found in db, querying openstack
        hypervisors = Hypervisors(api_session=admin_session).get_hypervisors(region=instance.instance.region)
        for hypervisor in hypervisors:
            if hypervisor.hypervisor_hostname == hypervisor_name:
                return {
                    'type': hypervisor.hypervisor_type,
                    'ip': hypervisor.host_ip
                }

    @action(detail=True, methods=['get'])
    def get_console_url(self, request, id):
        instance = self.get_admin_instance()
        instance_details = instance.api_instance.to_dict()
        instance_internal_name = instance_details.get('OS-EXT-SRV-ATTR:instance_name')
        hypervisor_name = instance_details.get('OS-EXT-SRV-ATTR:hypervisor_hostname')
        tenant_id = instance.instance.project.project_id
        admin_session = self.identity_admin_api.session

        hypervisor_details = self.get_instance_hypervisor_details(
            instance=instance,
            admin_session=admin_session,
            hypervisor_name=hypervisor_name,
        )
        if hypervisor_details['type'] == 'lxd':
            if not settings.ENABLE_LXC_CONSOLE:
                raise APIBadRequest(
                    detail=_('LXC console is disabled. Unable to open console for instance {0}').format(
                        instance.instance.name
                    )
                )

            response_data = {
                'url': self.get_lxc_console_url(
                    hypervisor_name,
                    hypervisor_details['ip'],
                    instance_internal_name,
                    instance.instance.id,
                    tenant_id,
                ),
                'lxc': True
            }
        else:
            try:
                response_data = instance.get_vnc_url()
            except (Exception, UnsupportedConsoleType):
                try:
                    response_data = instance.get_spice_url()
                except (Exception, UnsupportedConsoleType):
                    LOG.error('Unable to connect to VNC or Spice console for instance {}.'.format(instance.instance.id))
                    raise APIBadRequest(
                        detail=_('Unable to connect to VNC or Spice console for instance {}.').format(
                            instance.instance.name,
                        )
                    )

        return Response(response_data)

    @action(detail=True, methods=['post'])
    def reboot(self, request, *args, **kwargs):
        instance = self.get_instance()
        # TODO(tomo): Handle possible not found errors
        try:
            instance.reboot()
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to reboot instance {0}').format(instance.instance.name)
            handle(request, message=msg)
        return Response({'detail': _('Rebooting')})

    @action(detail=True, methods=['post'])
    def rename(self, request, id):
        serializer = instance_serializers.InstanceNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_instance()
        try:
            instance.rename(new_name=serializer.validated_data['name'])
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to rename instance {0}').format(instance.instance.name)
            handle(self.request, message=msg)
        return Response({'detail': _('Renamed')})

    @action(detail=True, methods=['get'])
    def get_snapshot_price(self, request, id):
        del request, id  # unused
        instance = self.get_object()  # type: InstanceModel
        service = instance.project.service
        pricing_plan = service.service_dynamic_usage.plan

        display_time_unit = settings.INSTANCE_SNAPSHOT_PRICE_TIME_UNIT
        display_attribute_unit = settings.INSTANCE_SNAPSHOT_PRICE_ATTRIBUTE_UNIT

        price_per_storage = MonetaryAmount(Decimal(0), pricing_plan.currency)
        price_per_snapshot = MonetaryAmount(Decimal(0), pricing_plan.currency)

        for pricing_rule in pricing_plan.pricing_rules.all():
            if pricing_rule.resource_name == 'image' and pricing_rule.resource_type == 'service':
                rule_price_calculator = RulePriceCalculator(pricing_rule, pricing_rule.plan.currency)
                if rule_price_calculator.attribute_unit:
                    price_per_storage += rule_price_calculator.get_max_price(
                        time_unit=display_time_unit,
                        attribute_unit=display_attribute_unit,
                    )
                else:
                    price_per_snapshot += rule_price_calculator.get_max_price(
                        time_unit=display_time_unit,
                        attribute_unit=display_attribute_unit,
                    )

        return Response({
            # TODO: handle attributes units
            'price_per_storage': '{} / {} / {}'.format(
                price_per_storage.format(settings.INSTANCE_SNAPSHOT_PRICE_PREC),
                VALUE_UNIT_MAP[display_attribute_unit],
                TIME_UNIT_MAP[display_time_unit],
            ) if price_per_storage.value > 0 else None,
            'price_per_snapshot': ' {} / {}'.format(
                price_per_snapshot.format(settings.INSTANCE_SNAPSHOT_PRICE_PREC),
                TIME_UNIT_MAP[display_time_unit],
            ) if price_per_snapshot.value > 0 else None,
        })

    @action(detail=True, methods=['post'])
    def create_snapshot(self, request, id):
        serializer = instance_serializers.InstanceNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_instance()
        try:
            image_uuid = instance.create_snapshot(name=serializer.validated_data['name'])
            return Response({'image_uuid': image_uuid})
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to create snapshot for instance {0}').format(instance.instance.name)
            handle(self.request, message=msg)

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
            result = []
        except NotFound as e:
            LOG.exception(e)
            result = []
        except ClientException as e:
            LOG.exception(e)
            result = []
        except EndpointNotFound as e:
            LOG.exception(e)
            result = []
        except ConnectTimeout as e:
            LOG.exception(e)
            result = []

        return Response({'measures': result})

    @action(detail=True, methods=['GET'])
    def actions(self, request, id):
        """Return instance actions (create, resize, rename...)"""
        instance = self.get_instance()
        result = []
        try:
            result = instance.get_actions()
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to get actions for instance {0}').format(instance.instance.name)
            handle(self.request, message=msg)

        # try to paginate the results
        paginator = FleioPaginationSerializer()
        page = paginator.paginate_queryset(result, self.request, view=self)
        if page is not None:
            serializer = instance_serializers.InstanceActionsSerializer(many=True)
            result = paginator.get_paginated_response(serializer.to_representation(page))
            return Response(result.data)

        return Response(result)

    @action(detail=True, methods=['POST'])
    def change_password(self, request, id):
        if request.user.is_staff is True:
            password_change_enabled = staff_active_features.is_enabled('openstack.instances.allow_changing_password')
        else:
            password_change_enabled = active_features.is_enabled('openstack.instances.allow_changing_password')
        if not password_change_enabled:
            raise exceptions.APIBadRequest(_('Change instance password feature is disabled.'))
        serializer = instance_serializers.InstanceChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_instance()
        if instance.status == InstanceStatus.ACTIVE:
            try:
                instance.change_password(password=serializer.validated_data['password'])
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to change password for instance {0}').format(instance.instance.name)
                try:
                    instance.reset_state(state=InstanceStatus.ACTIVE)
                except Exception as e:
                    LOG.error(e)
                handle(request=self.request, message=msg)
            return Response({'detail': _('Changing password')})
        else:
            raise exceptions.APIBadRequest(_('Can only change password for instance with status ACTIVE'))

    @action(detail=True, methods=['POST'])
    def reset_state(self, request, id):
        instance = self.get_instance()
        if instance.status == InstanceStatus.ERROR:
            try:
                instance.reset_state(state=InstanceStatus.ACTIVE)
            except Exception as e:
                LOG.error(e)
                msg = _('Unable to reset state of instance {0}').format(instance.instance.name)
                handle(request, message=msg)
        return Response({'detail': 'reset_state'})

    @action(detail=True, methods=['POST'])
    def attach_volume(self, request, id):
        instance = self.get_instance()
        serializer = instance_serializers.VolumeIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        volume_id = serializer.validated_data['volume_id']
        try:
            instance.attach_volume(volume_id=volume_id)
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to attach the volume {0}').format(volume_id)
            handle(request, message=msg)
        return Response({'detail': _('Volume attaching')})

    @action(detail=True, methods=['POST'])
    def detach_volume(self, request, id):
        instance = self.get_instance()
        serializer = instance_serializers.VolumeIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        volume_id = serializer.validated_data['volume_id']
        try:
            instance.detach_volume(volume_id=volume_id)
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to detach the volume {0}').format(volume_id)
            handle(request, message=msg)
        return Response({'detail': _('Volume detaching')})

    @action(detail=True, methods=['post'])
    def add_floating_ip(self, request, id):
        serializer = instance_serializers.AddFloatingIpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_instance()
        floating_ip = serializer.validated_data['floating_ip']
        # TODO(erno): handle floating ip not found and tenant specific differently? (implement in handle)
        try:
            instance.add_floating_ip(floating_ip=floating_ip,
                                     fixed_ip=serializer.validated_data.get('fixed_ip', None))
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to add floating ip {ip} to instance {instance_name}')
            msg = msg.format(ip=floating_ip, instance_name=instance.instance.name)
            handle(self.request, message=msg)
        return Response({'detail': _('Floating ip associated')})

    @action(detail=True, methods=['post'])
    def remove_floating_ip(self, request, id):
        serializer = instance_serializers.IpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_instance()
        ip = serializer.validated_data['ip']
        # TODO(erno): handle floating ip not found differently?
        try:
            instance.remove_floating_ip(floating_ip=ip)
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to remove floating ip {ip} from instance {instance_name}')
            msg = msg.format(ip=ip, instance_name=instance.instance.name)
            handle(self.request, message=msg)
        return Response({'detail': _('Floating ip dissociated')})

    @action(detail=True, methods=['get'])
    def associate_ip_create_options(self, request, id):
        # get instance's ports keep the free ones
        # TODO(tomo): Filter by region and ports that can actually connect to a floating IP
        # the problem here is that an instance port can be connected to an isolated network
        # without a router. We currently allow setting a floating IP to any available ports
        # which is not ok (and which will actually throw an error from Openstack APIs).
        db_instance = self.get_object()
        ports = Port.objects.filter(device_id=db_instance.id).exclude(
            id__in=FloatingIp.objects.filter(port__device_id=db_instance.id).values_list('port_id'))
        ports = PortSerializer(ports, many=True).data
        free_floating_ips = FloatingIpSerializer(
            FloatingIp.objects.filter(
                port__sync_version=None,  # NOTE: we use sync_version field to determine if port actually exists
                # because of the db_constraint=False on port field from FloatingIp model
                project_id=db_instance.project_id,
                floating_network__region=db_instance.region),
            many=True
        ).data
        if not ports:
            raise exceptions.APIConflict(detail=_('No free ports available'))
        if not free_floating_ips:
            raise exceptions.APIConflict(detail=_('No free floating IPs available'))
        return Response({'ports': ports, 'free_ips': free_floating_ips})

    @action(detail=True, methods=['get'])
    def dissociate_ip_create_options(self, request, id):
        # get instance's associated ports
        db_instance = self.get_object()
        ips = FloatingIp.objects.filter(port__device_id=db_instance.id)
        if not ips:
            raise exceptions.APIBadRequest(detail=_('No ports are associated'))
        return Response({'ips': FloatingIpSerializer(ips, many=True).data})

    @action(detail=True, methods=['get'])
    def list_security_groups(self, request, id):
        instance = self.get_instance()
        security_groups_lists = Port.objects.filter(device_id=instance.instance.id).values_list('security_groups')
        sec_list = list()
        for security_group_list in security_groups_lists:
            sec_list += [x for x in json.loads(security_group_list[0])]
        security_groups = list()
        if sec_list:
            sec_set = set(sec_list)
            # NOTE(erno): for the user we don't list security groups other than the project's security groups
            # this behaviour is also found in horizon
            try:
                sec_groups = SecurityGroup.objects.filter(id__in=sec_set, project=instance.instance.project)
            except Project.DoesNotExist:
                sec_groups = []

            for sec_group in sec_groups:
                security_group_rules = list()
                for rule in sec_group.security_group_rules.all():
                    security_group_rules.append({'display': self._format_security_rule(rule.__dict__)})
                security_groups.append({'id': sec_group.id, 'name': sec_group.name,
                                        'description': sec_group.description,
                                        'security_group_rules': security_group_rules})
        return Response({'security_groups': security_groups})

    @staticmethod
    def _format_security_rule(sgr):
        if not sgr['remote_ip_prefix'] and not sgr['remote_group_id']:
            if sgr['ethertype'] == 'IPv6':
                sgr['remote_ip_prefix'] = '::/0'
            else:
                sgr['remote_ip_prefix'] = '0.0.0.0/0'

        cidr = sgr['remote_ip_prefix']
        sgr['ip_range'] = {'cidr': cidr} if cidr else {}

        if 'cidr' in sgr['ip_range']:
            remote = sgr['ip_range']['cidr']
        else:
            remote = 'ANY'
        direction = 'to' if sgr['direction'] == 'egress' else 'from'
        if sgr['port_range_min']:
            if sgr['port_range_min'] == sgr['port_range_max']:
                proto_port = ("{}/{}".format(sgr['port_range_min'], sgr['protocol'].lower()))
            else:
                proto_port = ("{}-{}/{}".format(sgr['port_range_min'], sgr['port_range_max'], sgr['protocol'].lower()))
        elif sgr['protocol']:
            try:
                ip_proto = int(sgr['protocol'])
                proto_port = "ip_proto={}".format(ip_proto)
            except ValueError:
                # well-defined IP protocol name like TCP, UDP, ICMP.
                proto_port = sgr['protocol']
        else:
            proto_port = ''

        return _('Allow {ethertype} {proto_port} {direction} {remote}') \
            .format(ethertype=sgr['ethertype'], proto_port=proto_port, remote=remote, direction=direction)

    @action(detail=True, methods=['post'])
    def associate_security_group(self, request, id):
        try:
            group = request.data['group']
        except KeyError:
            raise exceptions.APIBadRequest(detail=_('Parameter "group" required'))

        instance = self.get_instance()
        try:
            instance.associate_security_group(group=group)
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to associate security group {group} to instance {instance_name}')
            msg = msg.format(group=group, instance_name=instance.instance.name)
            handle(self.request, message=msg)
        return Response({'detail': _('Security group associated')})

    @action(detail=True, methods=['get'])
    def associate_security_group_create_options(self, request, id):
        instance = self.get_object()
        try:
            security_groups_lists = Port.objects.filter(device_id=instance.id).values_list('security_groups')
            sec_list = list()
            for security_group_list in security_groups_lists:
                sec_list += [x for x in json.loads(security_group_list[0])]
            sec_set = set(sec_list)
        except Exception as e:  # try/except used only for debugging
            LOG.exception(e)
            sec_set = set(list())
        try:
            security_groups = SecurityGroup.objects.filter(project=instance.project, region__id=instance.region)
            security_groups = security_groups.exclude(id__in=sec_set)
        except Project.DoesNotExist:
            security_groups = []
        return Response({'groups': [{'id': sec_group.id, 'name': sec_group.name} for sec_group in security_groups]})

    @action(detail=True, methods=['post'])
    def dissociate_security_group(self, request, id):
        try:
            group = request.data['group']
        except KeyError:
            raise exceptions.APIBadRequest(detail=_('Parameter "group" required'))

        instance = self.get_instance()
        try:
            instance.dissociate_security_group(group=group)
        except Exception as e:
            LOG.error(e)
            msg = _('Unable to dissociate security group {group} to instance {instance_name}')
            msg = msg.format(group=group, instance_name=instance.instance.name)
            handle(self.request, message=msg)
        return Response({'detail': _('Security group associated')})

    @action(detail=True, methods=['POST'])
    def create_backup(self, request, id):
        if not active_features.is_enabled('openstack.osbackup'):
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
        if not active_features.is_enabled('openstack.osbackup'):
            raise APIBadRequest(_('Backup feature is disabled.'))
        del request  # unused
        instance = self.get_instance()
        backup_schedules_qs = OpenStackBackupSchedule.objects.filter(instance__id=instance.uuid)
        backups = Image.objects.filter(type='backup', instance_uuid=instance.uuid)
        return Response({
            'schedules': BackupScheduleSerializer(instance=backup_schedules_qs, many=True).data,
            'backups': images_serializers.ImageBriefSerializer(instance=backups, many=True).data,
        })

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=True, methods=['get'])
    def add_ip_options(self, request, id):
        instance = self.get_instance()
        instance_region = instance.instance.region
        networks = Network.objects.get_networks_for_project(
            project_id=instance.instance.project_id,
            external=True,
            subnet_count=True
        ).filter(subnet_count__gt=0, region=instance_region)

        ports = Port.objects.filter(device_id=id)
        if not networks:
            raise ObjectNotFound({'detail': _('No networks found for project')})
        if not hasattr(instance.instance, 'project_id'):
            raise APIConflict({'detail': _('Instance has no project')})
        if not ports:
            raise ObjectNotFound({'detail': _('No ports found for instance')})
        return Response(
            {
                'networks': NetworkSerializerExtra(networks, many=True, context={'request': request}).data,
                'ports': PortSerializer(ports, many=True).data,
            })

    @action(detail=True, methods=['get'])
    def add_port_options(self, request, id):
        instance = self.get_instance()
        instance_region = instance.instance.region
        networks = Network.objects.get_networks_for_project(
            project_id=instance.instance.project_id,
            external=True,
            subnet_count=True,
        ).filter(subnet_count__gt=0, region=instance_region)
        if not networks:
            raise ObjectNotFound({'detail': _('No networks found for project')})
        if not hasattr(instance.instance, 'project_id'):
            raise APIConflict({'detail': _('Instance has no project')})
        return Response(
            {
                'networks': NetworkSerializerExtra(networks, many=True, context={'request': request}).data,
                'project_id': instance.instance.project_id,
            })
