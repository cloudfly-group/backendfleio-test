from __future__ import unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from neutronclient.common.exceptions import BadRequest
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.permissions.permissions_cache import permissions_cache

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import handle
from fleio.openstack.models import SubnetPool
from fleio.openstack.networking.api import SubnetPools
from fleio.openstack.views.regions import get_regions
from .serializers import StaffSubnetPoolCreateSerializer, StaffSubnetPoolSerializer, StaffSubnetPoolUpdateSerializer
from fleio.core.filters import CustomFilter

LOG = logging.getLogger(__name__)


class StaffSubnetPoolViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSubnetPoolSerializer
    serializer_map = {'create': StaffSubnetPoolCreateSerializer,
                      'update': StaffSubnetPoolUpdateSerializer}
    permission_classes = (CustomPermissions, StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    ordering_fields = ('name', 'created_at', 'region', 'prefixes')
    search_fields = ('name', 'created_at', 'region', 'prefixes')

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def get_queryset(self):
        return SubnetPool.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        subnet_pool_admin_api = SubnetPools(api_session=self.identity_admin_api.session)
        try:
            subnet_pool = subnet_pool_admin_api.create(kwargs=serializer.validated_data)
            serializer.validated_data.update(subnet_pool['subnetpool'])
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create subnet pool'))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        subnet_pool_admin_api = SubnetPools(api_session=self.identity_admin_api.session)
        try:
            subnet_pool = subnet_pool_admin_api.update(id=serializer.instance.id, region=serializer.instance.region,
                                                       kwargs=serializer.validated_data)
            serializer.validated_data.update(subnet_pool['subnetpool'])
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update subnet pool'))

    def get_subnet_pool(self, subnet_pool=None):
        subnet_pool = subnet_pool or self.get_object()
        subnet_pool_admin_api = SubnetPools(api_session=self.identity_admin_api.session)
        return subnet_pool_admin_api.get(subnet_pool=subnet_pool)

    def perform_destroy(self, db_subnet_pool):
        """Delete subnet pool from neutron and from db."""
        subnet_pool = self.get_subnet_pool()
        try:
            subnet_pool.delete(region=db_subnet_pool.region)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=e)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        selected_region, regions = get_regions(request)
        return Response({'regions': regions, 'selected_region': selected_region})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
