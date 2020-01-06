from django_filters.rest_framework import FilterSet

from fleio.openstack.models import Network


class NetworkFilter(FilterSet):
    class Meta:
        model = Network
        fields = ('name', 'created_at', 'region')
