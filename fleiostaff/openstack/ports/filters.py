import django_filters

from fleio.openstack.models import Port


class PortFilters(django_filters.FilterSet):
    class Meta:
        model = Port
        fields = ('name', 'device_id', 'device_owner', 'network_id')
