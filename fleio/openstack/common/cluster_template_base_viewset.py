import logging

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import CustomPermissions
from fleio.core.exceptions import APIBadRequest
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.openstack.exceptions import ForbiddenException
from fleio.openstack.images.serializers import ImageSerializer
from fleio.openstack.instances.serializers import FlavorSerializer

from fleio.openstack.container_infra.cluster_templates.serializers import ClusterTemplateListSerializer
from fleio.openstack.container_infra.cluster_templates.serializers import ClusterTemplateSerializer
from fleio.openstack.container_infra.cluster_templates.serializers import ClusterTemplateCreateSerializer
from fleio.core.filters import CustomFilter
from fleio.openstack.networking.serializers import NetworkSerializer, SubnetSerializer
from fleio.openstack.osapi import OSApi
from fleio.openstack.serializers.regions import RegionSerializer
from fleio.pkm.serializers import PublicKeySerializer
from fleiostaff.openstack.osadminapi import OSAdminApi

LOG = logging.getLogger(__name__)

COE_DISTROS_FILTERS = {
    'kubernetes': Q(os_distro='fedora-atomic') | Q(os_distro='coreos'),
    'mesos': Q(os_distro='ubuntu'),
    'swarm': Q(os_distro='fedora-atomic'),
}


class ClusterTemplateBaseViewSet(viewsets.ModelViewSet):
    serializer_class = ClusterTemplateSerializer
    serializer_map = {
        'list': ClusterTemplateListSerializer,
        'retrieve': ClusterTemplateSerializer,
        'create': ClusterTemplateCreateSerializer,
    }
    permission_classes = (CustomPermissions,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('name', 'id')
    filter_fields = ('project_id',)

    def get_queryset(self):
        raise NotImplementedError()

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    def get_images_for_coe_qs(self, region=None, request=None):
        raise NotImplementedError()

    @staticmethod
    def get_keypairs_qs(request=None):
        raise NotImplementedError()

    def get_flavors_qs(self, region=None, request=None):
        raise NotImplementedError()

    @staticmethod
    def get_regions_qs():
        raise NotImplementedError()

    def get_networks_qs(self, region=None, request=None):
        raise NotImplementedError()

    def get_subnets_qs(self, region=None, request=None):
        raise NotImplementedError()

    def get_os_api(self, request):
        raise NotImplementedError()

    @staticmethod
    def get_project_id(request=None):
        raise NotImplementedError()

    def perform_create(self, serializer):
        if serializer.validated_data.get('public', False) is True and self.request.user.is_staff is False:
            raise ForbiddenException(_('You are not allowed to create a public cluster template'))
        os_api = self.get_os_api(request=self.request)  # type: [OSApi, OSAdminApi]
        try:
            return os_api.cluster_templates.create(
                **serializer.validated_data,
            )
        except Exception as e:
            raise APIBadRequest(str(e))

    def perform_destroy(self, instance):
        if self.request.user.is_staff is False:
            user_project_id = self.get_project_id(request=self.request)
            if instance.project.project_id != user_project_id and instance.public is True:
                raise ForbiddenException(_('You are not allowed to delete a public cluster template.'))
        os_api = self.get_os_api(request=self.request)  # type: [OSApi, OSAdminApi]
        os_cluster_template = os_api.cluster_templates.get(cluster_template=instance)
        try:
            os_cluster_template.delete()
        except Exception as e:
            raise APIBadRequest(str(e))
        return Response({'detail': _('Successfully deleted cluster template')})

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        region_name = request.query_params.get('region', None)
        image_qs = self.get_images_for_coe_qs(region=region_name, request=request)
        images_for_kubernetes = image_qs.filter(COE_DISTROS_FILTERS.get('kubernetes'))
        images_for_swarm = image_qs.filter(COE_DISTROS_FILTERS.get('swarm'))
        images_for_mesos = image_qs.filter(COE_DISTROS_FILTERS.get('mesos'))
        keypairs = self.get_keypairs_qs(request=request)
        flavors = self.get_flavors_qs(region=region_name, request=request)
        regions = self.get_regions_qs()
        networks = self.get_networks_qs(region=region_name, request=request)
        external_networks = networks.filter(router_external=True)
        private_networks = networks.filter(router_external=False)
        subnets_qs = self.get_subnets_qs(region=region_name, request=request)
        fixed_subnets = subnets_qs.filter(network__router_external=False)
        return Response({
            'kubernetes_images': ImageSerializer(images_for_kubernetes, many=True).data,
            'swarm_images': ImageSerializer(images_for_swarm, many=True).data,
            'mesos_images': ImageSerializer(images_for_mesos, many=True).data,
            'keypairs': PublicKeySerializer(keypairs, many=True).data,
            'flavors': FlavorSerializer(flavors, many=True).data,
            'regions': RegionSerializer(regions, many=True).data,
            'external_networks': NetworkSerializer(external_networks, many=True).data,
            'private_networks': NetworkSerializer(private_networks, many=True).data,
            'fixed_subnets': SubnetSerializer(fixed_subnets, many=True).data,
        })

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        regions = self.get_regions_qs()
        return Response({
            'regions': RegionSerializer(regions, many=True).data,
        })
