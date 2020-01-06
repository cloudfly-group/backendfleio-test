from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import NumberFilter
from rest_framework import filters
from rest_framework import viewsets

from fleio.billing.models import Journal
from fleio.core.drf import ResellerOnly
from fleio.core.filters import CustomFilter
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.billing.journal.serializers import StaffJournalDetailsSerializer


class JournalFilter(FilterSet):
    client_id = NumberFilter(method='filter_by_client_id')

    class Meta:
        model = Journal
        fields = [
            'invoice',
            'transaction',
            'source',
            'destination',
            'client_id',
        ]

    @staticmethod
    def filter_by_client_id(queryset, name, value):
        del name  # unused
        return queryset.filter(Q(invoice__client_id=value) | Q(client_credit__client_id=value))


class JournalViewset(viewsets.ModelViewSet):
    serializer_class = StaffJournalDetailsSerializer
    permission_classes = (ResellerOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_class = JournalFilter
    ordering_fields = ('id', 'invoice', 'transaction', 'transaction__status', 'source', 'destination',
                       'source_amount', 'destination_amount')
    search_fields = (
        'id', 'invoice__id', 'transaction__external_id', 'source', 'destination',
        'source_amount', 'destination_amount', 'transaction__currency__code', 'user__first_name',
        'user__last_name', 'invoice__client__first_name', 'invoice__client__last_name', 'invoice__client__company',
        'client_credit__client__first_name', 'client_credit__client__last_name', 'client_credit__client__company'
    )
    ordering = ['-date_added']

    def get_queryset(self):
        reseller_resources = user_reseller_resources(self.request.user)
        return Journal.objects.filter(
            Q(client_credit__client__reseller_resources=reseller_resources) |
            Q(invoice__client__reseller_resources=reseller_resources)
        ).all()
