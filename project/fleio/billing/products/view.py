from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from fleio.billing.models import Product
from fleio.billing.products.serializers import ProductSerializer
from fleio.core.features import active_features
from fleio.core.models import get_default_currency


class ProductViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('code', 'group', 'product_type', 'status', 'price_model', 'auto_setup', 'taxable')
    ordering_fields = ('name', 'available_quantity', 'status', 'next_due_date')
    search_fields = ('name', 'code', 'status', 'group', 'product_type')

    def get_currency_or_default(self):
        if self.request and self.request.user.is_authenticated:
            client = self.request.user.clients.first()
            if client:
                currency = client.currency
            else:
                currency = get_default_currency()
        else:
            currency = get_default_currency()
        return currency

    def get_queryset(self):
        currency = self.get_currency_or_default()
        qs = Product.objects.filter(
            (Q(group__visible=True) & (Q(module__plugin__enabled=True) | Q(module__plugin=None)))
        )
        qs = qs.exclude(module__plugin__feature_name__in=active_features.get_disabled_features())
        return qs.available_for_order(currency=currency)
