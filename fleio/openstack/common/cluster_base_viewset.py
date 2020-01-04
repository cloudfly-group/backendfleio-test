import copy
import io
import logging

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from novaclient.exceptions import Conflict
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import CustomPermissions
from fleio.core.exceptions import APIBadRequest
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.openstack.api import identity
from fleio.openstack.api.nova import nova_client
from fleio.openstack.instances.serializers import FlavorSerializer
from fleio.openstack.models import Cluster, ClusterTemplate

from fleio.openstack.container_infra.clusters import serializers
from fleio.core.filters import CustomFilter
from fleio.openstack.models.cluster import ClusterStatus
from fleio.openstack.osapi import OSApi
from fleio.openstack.serializers.regions import RegionSerializer
from fleio.openstack.utils import newlines_substract
from fleio.pkm.models import PublicKey
from fleio.pkm.serializers import PublicKeySerializer
from fleio.utils.model import statuses_dict_to_statuses_choices
from fleiostaff.openstack.osadminapi import OSAdminApi

LOG = logging.getLogger(__name__)


class ClusterBaseViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.ClusterSerializer
    serializer_map = {
        'list': serializers.ClusterListSerializer,
        'retrieve': serializers.ClusterSerializer,
        'create': serializers.ClusterCreateSerializer,
        'resize_cluster': serializers.ClusterResizeSerializer,
    }
    permission_classes = (CustomPermissions,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('name', 'status', 'id')
    filter_fields = ('cluster_template',)

    def get_queryset(self):
        return Cluster.objects.all()

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    @staticmethod
    def get_keypairs_qs(request=None):
        raise NotImplementedError()

    def get_flavors_qs(self, region=None, request=None):
        raise NotImplementedError()

    @staticmethod
    def get_os_api(request):
        raise NotImplementedError()

    @staticmethod
    def get_project_id(request=None):
        raise NotImplementedError()

    @staticmethod
    def get_regions_qs():
        raise NotImplementedError()

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        cluster_template_id = request.query_params.get('cluster_template_id', None)
        cluster_template = ClusterTemplate.objects.filter(id=cluster_template_id).first()
        if not cluster_template:
            return Response({})
        region = cluster_template.region
        flavors = self.get_flavors_qs(region=region, request=request)
        keypairs = self.get_keypairs_qs(request=request)
        return Response({
            'flavors': FlavorSerializer(flavors, many=True).data,
            'keypairs': PublicKeySerializer(keypairs, many=True).data,
        })

    def perform_create(self, serializer):
        os_api = self.get_os_api(request=self.request)  # type: [OSApi, OSAdminApi]
        serialized_data = copy.deepcopy(serializer.validated_data)
        cluster_template_id = serialized_data.get('cluster_template_id')
        keypair_name = serialized_data.pop('keypair')
        keypair = PublicKey.objects.filter(user=self.request.user, name=keypair_name).first()
        if not keypair:
            if self.request.user.is_staff:
                msg = _('Provided keypair was not found or you do not own it.')
            else:
                msg = _('Provided keypair was not found.')
            raise APIBadRequest(msg)
        keypair_name_formatted = '{}_{}'.format(keypair_name, self.get_project_id(request=self.request))
        if not cluster_template_id:
            raise APIBadRequest(_('You need to provide a cluster template'))
        cluster_template = ClusterTemplate.objects.filter(id=cluster_template_id).first()
        if not cluster_template:
            raise APIBadRequest(_('Provided cluster template cannot be found anymore'))
        nc = nova_client(api_session=identity.IdentityAdminApi().session, region_name=cluster_template.region)
        try:
            nc.keypairs.create(
                name=keypair_name_formatted,
                public_key=newlines_substract(keypair.public_key)
            )
        except Conflict:
            # Key was created before, use it
            try:
                return os_api.clusters.create(
                    region_id=cluster_template.region,
                    keypair=keypair_name_formatted,
                    **serialized_data,
                )
            except Exception as e:
                raise APIBadRequest(str(e))
        except Exception as e:
            raise APIBadRequest(str(e))
        try:
            return os_api.clusters.create(
                region_id=cluster_template.region,
                keypair=keypair_name_formatted,
                **serialized_data,
            )
        except Exception as e:
            raise APIBadRequest(str(e))

    def perform_destroy(self, instance):
        os_api = self.get_os_api(request=self.request)  # type: [OSApi, OSAdminApi]
        os_cluster = os_api.clusters.get(cluster=instance)
        try:
            os_cluster.delete()
        except Exception as e:
            raise APIBadRequest(str(e))
        return Response({'detail': _('Successfully deleted cluster')})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=True, methods=['get'])
    def get_certificate(self, request, pk):
        db_cluster = self.get_object()
        os_api = self.get_os_api(request=request)  # type: [OSApi, OSAdminApi]
        os_cluster = os_api.clusters.get(cluster=db_cluster)
        try:
            certificate = os_cluster.get_certificate()
        except Exception as e:
            raise APIBadRequest(str(e))
        pem = certificate.pem
        file = io.StringIO()
        file.write(pem)
        response = HttpResponse(file.getvalue(), content_type='application/x-x509-ca-cert')
        file.close()
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('{}_ca.pem'.format(db_cluster.name))
        return response

    @action(detail=True, methods=['post'])
    def resize_cluster(self, request, pk):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        node_count = serializer.validated_data.get('node_count', 1)
        nodes_to_remove = serializer.validated_data.get('nodes_to_remove', [])
        db_cluster = self.get_object()
        if db_cluster.status in ClusterStatus.under_progress_statuses:
            raise APIBadRequest(_('Cluster is already under a task.'))
        os_api = self.get_os_api(request=request)  # type: [OSApi, OSAdminApi]
        os_cluster = os_api.clusters.get(cluster=db_cluster)
        try:
            os_cluster.resize(node_count=node_count, nodes_to_remove=nodes_to_remove)
        except Exception as e:
            raise APIBadRequest(str(e))
        return Response({'detail': _('Cluster resize started')})

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        regions = self.get_regions_qs()
        return Response({
            'regions': RegionSerializer(regions, many=True).data,
            'statuses': statuses_dict_to_statuses_choices(dictionary=ClusterStatus.choices.items()),
        })
