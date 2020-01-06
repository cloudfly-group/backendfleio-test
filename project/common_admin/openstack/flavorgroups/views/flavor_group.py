from django.db.models.deletion import ProtectedError
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common_admin.openstack.flavorgroups.serializers import AdminFlavorGroupSerializer
from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.openstack.models import FlavorGroup
from fleio.openstack.models import Image


class AdminFlavorGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserOnly,)
    model = FlavorGroup
    queryset = FlavorGroup.objects.all()
    serializer_class = AdminFlavorGroupSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'description')
    ordering_fields = ('id', 'name', 'created_at', 'priority')

    @action(detail=False, methods=['get'])
    def get_available_flavor_groups_for_image(self, request):
        image_id = request.query_params.get('image_id')
        search = request.query_params.get('search')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavor groups against it'))
        try:
            Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))
        queryset = FlavorGroup.objects.all()
        queryset = queryset.exclude(images__id=image_id)
        if search:
            queryset = queryset.filter(name__icontains=search)
        objects = AdminFlavorGroupSerializer(instance=queryset, many=True, read_only=True).data
        return Response({'objects': objects})

    @action(detail=False, methods=['get'])
    def get_flavor_groups_assigned_to_image(self, request):
        image_id = request.query_params.get('image_id')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavor groups against it'))
        try:
            Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))
        queryset = FlavorGroup.objects.filter(images__id=image_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AdminFlavorGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AdminFlavorGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_image(self, request, pk):
        del pk  # unused

        flavor = self.get_object()  # type: FlavorGroup

        image_id = request.data.get('image_id')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavor groups against it'))
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))

        flavor.images.add(image)
        flavor.save()

        return Response({'detail': _('Flavor group added to image')})

    @action(detail=True, methods=['post'])
    def remove_from_image(self, request, pk):
        del pk  # unused

        flavor = self.get_object()  # type: FlavorGroup

        image_id = request.data.get('image_id')
        if not image_id:
            raise APIBadRequest(_('Missing image id to filter flavor groups against it'))
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            raise APIBadRequest(_('No image to filter against'))

        flavor.images.remove(image)
        flavor.save()

        return Response({'detail': _('Flavor group removed from image')})

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise APIBadRequest(_('Cannot delete flavor group while it has flavors associated with it.'))
