import logging

from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from novaclient.exceptions import NotFound
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import ForbiddenException
from fleio.core.features import staff_active_features
from fleio.core.filters import CustomFilter
from fleio.core.models import ClientGroup
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import handle
from fleio.openstack.flavor import Flavors
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.models import FlavorGroup
from fleio.openstack.models import Image
from fleio.openstack.models import Instance
from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.openstack.views.regions import get_regions
from fleiostaff.core.clientgroups.serializers import ClientGroupsMinSerializer
from fleiostaff.openstack.flavors.filters import OpenStackFlavorFilter
from fleiostaff.openstack.flavors.serializers import FlavorSerializer
from fleiostaff.openstack.flavors.serializers import FlavorUpdateSerializer
from fleiostaff.openstack.signals import staff_delete_flavor

LOG = logging.getLogger(__name__)


class AdminFlavorViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = FlavorSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = (
        'name',
        'description',
        'memory_mb',
        'root_gb',
        'region__id',
        'vcpus',
        'flavor_group__name',
    )
    ordering_fields = ('name', 'id', 'vcpus', 'memory_mb', 'root_gb', 'flavor_group')
    filter_class = OpenStackFlavorFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    @staticmethod
    def update_or_create(key, count, dictionary):
        val = dictionary.get(key, None)
        if val:
            dictionary[key] = dictionary[key] + count
        else:
            dictionary[key] = count
        return dictionary

    def get_queryset(self):
        return OpenstackInstanceFlavor.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return FlavorUpdateSerializer
        else:
            return FlavorSerializer

    def perform_update(self, serializer):
        if serializer.partial:
            serializer.save()
        else:
            preserve_id = serializer.validated_data.get('preserve_id', False)
            flavor_id = serializer.instance.id if preserve_id else None

            self.perform_destroy(serializer.instance)
            self.perform_create(serializer, region=serializer.instance.region.id, flavor_id=flavor_id)

    @action(detail=True, methods=['post'])
    def set_properties(self, request, pk):
        del pk  # unused

        db_flavor = self.get_object()
        new_properties = request.data.get('new_properties', {})
        flavors_api = Flavors(api_session=self.identity_admin_api.session)
        flavor_api = flavors_api.get(flavor=db_flavor)
        flavor_api.set_properties(new_properties=new_properties)
        return Response({'detail': _('Properties set')})

    @action(detail=True, methods=['post'])
    def unset_property(self, request, pk):
        del pk  # unused
        db_flavor = self.get_object()
        property_key = request.data.get('property_key', {})
        flavors_api = Flavors(api_session=self.identity_admin_api.session)
        flavor_api = flavors_api.get(flavor=db_flavor)
        try:
            flavor_api.unset_property(property_key=property_key)
        except NotFound:
            handle(self.request, message=_('Unable to remove flavor property'))
        return Response({'detail': _('Property unset')})

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        selected_region, regions = get_regions(request)
        return Response({'regions': regions, 'selected_region': selected_region})

    def perform_create(self, serializer, region=None, flavor_id=None):
        try:
            flavor_api = Flavors(api_session=self.identity_admin_api.session)
            create_parameters = {
                'name': serializer.validated_data['name'],
                'ram': serializer.validated_data['memory_mb'],
                'vcpus': serializer.validated_data['vcpus'],
                'disk': serializer.validated_data['root_gb'],
                'flavorid': serializer.validated_data.get('id', 'auto'),
                'ephemeral': serializer.validated_data['ephemeral_gb'],
                'swap': serializer.validated_data['swap'],
                'is_public': serializer.validated_data['is_public'],
                'region': region or serializer.validated_data['region'].id,
            }

            if flavor_id:
                create_parameters['flavorid'] = flavor_id

            flavor = flavor_api.create(**create_parameters)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create the flavor'))
        else:
            serializer.save(id=flavor.id, rxtx_factor=flavor.rxtx_factor,
                            disabled=getattr(flavor, "OS-FLV-DISABLED:disabled", False))

    def perform_destroy(self, db_flavor):
        """Delete flavor from nova and mark as deleted in Fleio db."""
        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        flavor_api = Flavors(api_session=self.identity_admin_api.session)
        flavor = flavor_api.get(flavor=db_flavor)
        try:
            pk = db_flavor.id
            flavor.delete()
            user = self.request.user
            staff_delete_flavor.send(sender=__name__, user=user, user_id=user.id,
                                     flavor_name=db_flavor.name, flavor_id=pk,
                                     username=user.username, request=self.request)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=e)

    @staticmethod
    def get_used_flavors_summary_queryset(user):
        return Instance.objects.values('flavor').annotate(
            count=Count('id')
        ).exclude(
            status=InstanceStatus.DELETED
        ).exclude(
            terminated_at__isnull=False
        ).order_by()

    @action(detail=False, methods=['get'])
    def summary(self, request):
        del request  # unused
        used_flavors = self.get_used_flavors_summary_queryset(user=self.request.user)
        flavors = OpenstackInstanceFlavor.objects.all()
        flavor_info = {}
        flavor_data = []
        flavor_labels = []
        for flavor in used_flavors:
            try:
                db_flavor = flavors.get(id=flavor['flavor'])
                flavor_info = self.update_or_create(db_flavor.name, flavor['count'], flavor_info)
            except OpenstackInstanceFlavor.DoesNotExist:
                flavor_info = self.update_or_create(flavor['flavor'], flavor['count'], flavor_info)

        for key, value in iter(flavor_info.items()):
            flavor_data.append(value)
            flavor_labels.append(key)
        return Response({'flavor_data': flavor_data, 'flavor_labels': flavor_labels})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=False, methods=['get'])
    def get_available_flavors_for_group(self, request):
        group_id = request.query_params.get('group')
        search = request.query_params.get('search')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter flavors against it'))
        try:
            FlavorGroup.objects.get(id=group_id)
        except FlavorGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))
        queryset = OpenstackInstanceFlavor.objects.all()
        queryset = queryset.exclude(flavor_group__isnull=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        objects = FlavorSerializer(instance=queryset, many=True, read_only=True).data
        return Response({'objects': objects})

    @action(detail=False, methods=['get'])
    def get_flavors_in_group(self, request):
        group_id = request.query_params.get('group_id')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter flavors against it'))
        try:
            group = FlavorGroup.objects.get(id=group_id)
        except FlavorGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))
        queryset = OpenstackInstanceFlavor.objects.filter(flavor_group=group)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FlavorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FlavorSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_group(self, request, pk):
        del pk  # unused

        flavor = self.get_object()  # type: OpenstackInstanceFlavor

        group_id = request.data.get('group_id')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter flavors against it'))
        try:
            group = FlavorGroup.objects.get(id=group_id)
        except FlavorGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))

        flavor.flavor_group = group
        flavor.save()

        return Response({'detail': _('Flavor added to group')})

    @action(detail=True, methods=['post'])
    def remove_from_group(self, request, pk):
        del pk  # unused

        flavor = self.get_object()  # type: OpenstackInstanceFlavor

        group_id = request.data.get('group_id')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter flavors against it'))
        try:
            group = FlavorGroup.objects.get(id=group_id)
            del group
        except FlavorGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))

        flavor.flavor_group = None
        flavor.save()

        return Response({'detail': _('Flavor removed from group')})

    @action(detail=False, methods=['get'])
    def get_available_flavors_for_image(self, request):
        image_id = request.query_params.get('image_id')
        search = request.query_params.get('search')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavors against it'))

        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))
        queryset = OpenstackInstanceFlavor.objects.filter(region=image.region)
        queryset = queryset.exclude(images__id=image_id)
        if search:
            queryset = queryset.filter(name__icontains=search)
        objects = FlavorSerializer(instance=queryset, many=True, read_only=True).data
        return Response({'objects': objects})

    @action(detail=False, methods=['get'])
    def get_flavors_assigned_to_image(self, request):
        image_id = request.query_params.get('image_id')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavors against it'))
        try:
            Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))
        queryset = OpenstackInstanceFlavor.objects.filter(images__id=image_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FlavorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FlavorSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_image(self, request, pk):
        del pk  # unused

        flavor = self.get_object()  # type: OpenstackInstanceFlavor

        image_id = request.data.get('image_id')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavors against it'))
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))

        flavor.images.add(image)
        flavor.save()

        return Response({'detail': _('Flavor added to image')})

    @action(detail=True, methods=['post'])
    def remove_from_image(self, request, pk):
        del pk  # unused

        flavor = self.get_object()  # type: OpenstackInstanceFlavor

        image_id = request.data.get('image_id')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavors against it'))
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))

        flavor.images.remove(image)
        flavor.save()

        return Response({'detail': _('Flavor removed from image')})

    @action(detail=False, methods=['get'])
    def get_available_client_groups_to_assign(self, request):
        """gets client groups not yet assigned to flavor"""
        flavor_id = request.query_params.get('flavor_id', None)
        if not flavor_id:
            raise APIBadRequest(_('Flavor id required.'))
        flavor = OpenstackInstanceFlavor.objects.filter(id=flavor_id).first()
        if not flavor:
            raise APIBadRequest(_('No flavor found for given id.'))
        search = request.query_params.get('search', None)
        qs = ClientGroup.objects.all().exclude(id__in=flavor.show_to_groups.values('id'))
        if search is not None:
            qs = qs.filter(name__icontains=search)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = ClientGroupsMinSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ClientGroupsMinSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_client_groups_related_to_flavor(self, request, pk):
        """gets client groups assigned to flavor"""
        flavor = self.get_object()
        qs = ClientGroup.objects.filter(id__in=flavor.show_to_groups.values('id'))
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = ClientGroupsMinSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ClientGroupsMinSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_client_group_to_flavor(self, request, pk):
        """assigns a client group to a flavor"""
        flavor = self.get_object()
        client_group_id = request.data.get('client_group', None)
        if not client_group_id:
            raise APIBadRequest(_('No client group id specified.'))
        client_group = ClientGroup.objects.filter(id=client_group_id).first()
        if not client_group:
            raise APIBadRequest(_('No client group found for assignment.'))
        if client_group in flavor.show_to_groups.all():
            raise APIBadRequest(_('Client group already assigned to this flavor.'))
        flavor.show_to_groups.add(client_group)
        return Response({'detail': _('Successfully assigned client group to flavor.')})

    @action(detail=True, methods=['post'])
    def remove_client_group_from_flavor(self, request, pk):
        """remove client group from flavor"""
        flavor = self.get_object()
        client_group_id = request.data.get('client_group', None)
        if not client_group_id:
            raise APIBadRequest(_('No client group id specified.'))
        client_group = ClientGroup.objects.filter(id=client_group_id).first()
        if not client_group:
            raise APIBadRequest(_('No client group found from given id.'))
        if client_group in flavor.show_to_groups.all():
            flavor.show_to_groups.remove(client_group)
            return Response({'detail': _('Successfully removed client group from flavor.')})
        else:
            raise APIBadRequest(_('Cannot remove client group from flavor as it is not assigned to it.'))
