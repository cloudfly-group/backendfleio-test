from django.db.models import Count
from django.db.models import Func


def annotate_clients_queryset(queryset):
    queryset = queryset.annotate(
        has_services=Func(Count('services'), function='SIGN')
    )
    queryset = queryset.annotate(
        has_instances=Func(Count('services__openstack_project__instance'), function='SIGN')
    )
    queryset = queryset.annotate(
        has_reseller_services=Func(Count('services__reseller_resources'), function='SIGN')
    )
    queryset = queryset.annotate(
        assigned_to_reseller=Func(Count('reseller_resources'), function='SIGN')
    )

    return queryset
