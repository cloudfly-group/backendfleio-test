import django_filters
from rest_framework import filters

from fleio.core.models import Client


class ClientFilter(django_filters.rest_framework.FilterSet):
    has_enabled_project = django_filters.BooleanFilter(
        field_name='openstack_project', method='filter_has_enabled_project',
    )
    has_reseller_service = django_filters.BooleanFilter(
        field_name='has_reseller_service', method='filter_has_reseller_service',
    )
    has_external_billing = django_filters.BooleanFilter(
        field_name='has_external_billing', method='filter_has_external_billing', distinct=True,
    )
    uptodate_credit_max = django_filters.NumberFilter(
        field_name='uptodate_credit_max', method='filter_uptodate_credit_max', distinct=True,
    )

    class Meta:
        model = Client
        fields = [
            'id', 'external_billing_id', 'has_enabled_project', 'has_billing_agreement', 'has_external_billing',
            'uptodate_credit_max'
        ]

    @staticmethod
    def filter_has_reseller_service(queryset, name, value):
        """Filter if user has reseller service or not"""
        del name  # unused

        return queryset.filter(services__reseller_resources__isnull=(not value))

    @staticmethod
    def filter_has_enabled_project(queryset, name, value):
        """
        Returns all clients with or without an openstack project
        Add '&' at the end of url when making the request
        E.g.: '../clients?has_enabled_project=True&'
        """
        del name  # unused
        if value is True:
            """returns all clients that have an openstack service"""
            return queryset.filter(services__openstack_project__disabled=False).distinct()
        else:
            """returns all clients without any openstack service"""
            return queryset.exclude(services__openstack_project__disabled=False).distinct()

    @staticmethod
    def filter_has_external_billing(queryset, name, value):
        """Filter is external billing is set or not"""
        del name  # unused

        qs = queryset
        if value:
            qs = qs.exclude(external_billing_id='')
        return qs.filter(external_billing_id__isnull=(not value))

    @staticmethod
    def filter_uptodate_credit_max(queryset, name, value):
        del name  # unused

        return queryset.filter(uptodate_credit__lt=value)


class OrderByIdLastFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering is not None:
            ordering.append('id')

        return ordering
