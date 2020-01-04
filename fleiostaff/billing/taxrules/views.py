from __future__ import unicode_literals

import pycountry
from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.billing.models import TaxRule
from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter
from fleio.openstack.exceptions import APIBadRequest
from fleiostaff.billing.taxrules.serializers import StaffTaxRuleCreateUpdateSerializer, StaffTaxRuleSerializer


class StaffTaxRuleViewset(viewsets.ModelViewSet):
    serializer_class = StaffTaxRuleSerializer
    model = TaxRule
    queryset = TaxRule.objects.all()
    serializer_map = {'create': StaffTaxRuleCreateUpdateSerializer,
                      'update': StaffTaxRuleCreateUpdateSerializer}
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('id', 'level', 'name', 'state', 'country', 'rate')
    ordering_fields = ('level', 'name', 'state', 'country', 'rate')
    search_fields = ('level', 'name', 'state', 'country', 'rate')
    ordering = ['country']

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        return Response({'countries': [country.name for country in pycountry.countries],
                         'levels': TaxRule.LEVELS})

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError as e:
            raise APIBadRequest(e)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError as e:
            raise APIBadRequest(e)
