from types import SimpleNamespace

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from fleio.core.drf import StaffOnly
from fleio.core.models import Currency
from fleio.core.filters import CustomFilter

from plugins.domains.models import TLD
from plugins.domains.models.tld import AddonPriceType
from plugins.domains.models.tld import PriceType
from plugins.domains.staff.serializers import DomainAddonPricesSerializer
from plugins.domains.staff.serializers import DomainPricesSerializer
from plugins.domains.staff.serializers import TLDSerializer


class TLDsViewSet(viewsets.ModelViewSet):
    serializer_class = TLDSerializer
    permission_classes = (
        StaffOnly,
    )
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, CustomFilter)
    search_fields = ('name',)
    ordering_fields = ('name', 'created_at', 'updated_at',)
    queryset = TLD.objects.all()

    @action(detail=True, methods=['get'])
    def get_prices(self, request: Request, pk) -> Response:
        del request, pk  # unused
        tld = self.get_object()

        domain_prices = SimpleNamespace()
        domain_prices.default_currency = Currency.objects.filter(is_default=True).first()
        domain_prices.price_types = PriceType.price_type_map
        domain_prices.price_cycles_list = tld.get_price_cycles_list()

        domain_prices_serializer = DomainPricesSerializer(
            instance=domain_prices
        )

        domain_addon_prices = SimpleNamespace()
        domain_addon_prices.default_currency = Currency.objects.filter(is_default=True).first()
        domain_addon_prices.price_types = AddonPriceType.price_type_map
        domain_addon_prices.price_cycles_list = tld.get_addon_price_cycles_list()

        domain_addon_prices_serializer = DomainAddonPricesSerializer(
            instance=domain_addon_prices
        )

        return Response(
            data={
                'domain_prices': domain_prices_serializer.data,
                'domain_addon_prices': domain_addon_prices_serializer.data,
            }
        )

    @action(detail=True, methods=['post'])
    def save_prices(self, request: Request, pk) -> Response:
        del pk  # unused
        tld = self.get_object()

        domain_prices = request.data.get('domain_prices', None)
        if domain_prices:
            domain_prices_serializer = DomainPricesSerializer(data=domain_prices)
            if domain_prices_serializer.is_valid(raise_exception=True):
                domain_prices_serializer.save_prices(tld=tld)

        domain_addon_prices = request.data.get('domain_addon_prices', None)
        if domain_addon_prices:
            domain_addon_prices_serializer = DomainAddonPricesSerializer(data=domain_addon_prices)
            if domain_addon_prices_serializer.is_valid(raise_exception=True):
                domain_addon_prices_serializer.save_prices(tld=tld)

        return Response()
