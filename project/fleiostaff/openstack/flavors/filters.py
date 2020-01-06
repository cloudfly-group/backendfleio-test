from django_filters.rest_framework import CharFilter, FilterSet

from fleio.openstack.models import OpenstackInstanceFlavor


class OpenStackFlavorFilter(FilterSet):
    name = CharFilter()

    class Meta:
        model = OpenstackInstanceFlavor
        fields = ['id', 'name']
