from django_filters.rest_framework import FilterSet

from fleio.openstack.models import Volume


class OpenStackVolumeFilter(FilterSet):
    class Meta:
        model = Volume
        fields = ['status', 'region']
