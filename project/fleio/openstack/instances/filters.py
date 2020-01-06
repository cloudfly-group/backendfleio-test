import ipaddress
import operator
import re

from django.db.models import Q
import django_filters
from functools import reduce
from rest_framework import filters
from fleio.openstack.models import Instance, Port


class InstanceFilter(django_filters.rest_framework.FilterSet):
    """Allow filtering of instances by client"""
    client = django_filters.CharFilter(field_name="project__service__client__id")

    class Meta:
        model = Instance
        fields = ['id', 'name', 'created', 'description', 'image', 'region', 'flavor', 'status', 'client']


class InstanceIpSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search')
        if search:
            try:
                ip_address = ipaddress.ip_address(search)  # type: ipaddress.IPv6Address
                if type(ip_address) is ipaddress.IPv6Address:
                    search = ip_address.compressed
            except ValueError:
                pass

        # for ipv4 minimum length to search is 3, for ipv6 is 4
        if search and len(search) > 2:
            parts = return_valid_ip_parts(search)
            if not parts:
                return super(InstanceIpSearchFilter, self).filter_queryset(request, queryset, view)
            instance_ids = queryset.values_list('id')
            # check if fixed ip contains a search term, couple with OR for multiple search terms
            query = reduce(
                operator.or_, (Q(fixed_ips__contains=item) | Q(floatingip__floating_ip_address=item) |
                               Q(floatingip__fixed_ip_address=item) for item in parts)
            )
            port_device_ids = Port.objects.filter(query, device_id__in=instance_ids).values_list('device_id')
            return queryset.filter(id__in=port_device_ids) | super(InstanceIpSearchFilter, self).filter_queryset(
                request, queryset, view)
        else:
            return super(InstanceIpSearchFilter, self).filter_queryset(request, queryset, view)


def return_valid_ip_parts(search):
    parts = search.split(' ')
    valid_parts = set()
    for part in parts:
        if len(part) > 2:
            ipv4_address_part = re.compile(r'^(\.?[0-9]{1,3}\.?)+$')
            if ipv4_address_part.match(part):
                valid_parts.add(part)
        if len(part) > 3:
            ipv6_address_part = re.compile(r'^([:]{0,2}[0-9a-fA-F]{0,4})+$')
            if ipv6_address_part.match(part):
                valid_parts.add(part)

    return valid_parts
