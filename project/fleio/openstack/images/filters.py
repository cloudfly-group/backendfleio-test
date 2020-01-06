from django_filters.rest_framework import CharFilter, FilterSet

from fleio.openstack.models import Image


class OpenStackImageFilter(FilterSet):
    name = CharFilter()

    class Meta:
        model = Image
        fields = ['instance_uuid', 'name', 'type']
