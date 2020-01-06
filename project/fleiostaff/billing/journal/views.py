from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import NumberFilter
from django.db.models import Q
from rest_framework import filters, viewsets

from fleio.billing.models import Journal
from fleio.core.drf import StaffOnly
from fleiostaff.billing.journal.serializers import StaffJournalDetailsSerializer
from fleio.core.filters import CustomFilter


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

    def filter_by_client_id(self, queryset, name, value):
        return queryset.filter(Q(invoice__client_id=value) | Q(client_credit__client_id=value))


class JournalViewset(viewsets.ModelViewSet):
    serializer_class = StaffJournalDetailsSerializer
    queryset = Journal.objects.all()
    permission_classes = (StaffOnly, )
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
