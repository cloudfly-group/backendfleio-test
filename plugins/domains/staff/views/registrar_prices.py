import logging

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fleio.core.drf import StaffOnly
from plugins.domains.models import RegistrarPrices
from plugins.domains.staff.serializers import RegistrarPricesSerializer
from plugins.domains.registrars_connectors.registrar_connector_manager import registrar_connector_manager

LOG = logging.getLogger(__name__)


class RegistrarPricesViewset(ModelViewSet):
    permission_classes = (StaffOnly, )
    queryset = RegistrarPrices.objects.all()
    serializer_class = RegistrarPricesSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('currency', 'tld_name', 'connector', 'years',)
    ordering_fields = ('currency', 'tld_name', 'connector', 'years', 'register_price', 'renew_price',
                       'transfer_price', 'promo_price', 'updated_at')
    search_fields = ('currency', 'tld_name', 'connector', 'years',)

    @action(methods=['POST'], detail=False)
    def update_prices(self, request):
        connector_name = request.data.get('connector')
        tld_name = request.data.get('tld_name', None)
        if connector_name:
            connector_info = registrar_connector_manager.connectors_info.get('connector_name', None)
            if not connector_info:
                raise ValidationError(detail=_('Connector {} not found').format(connector_name))
            connector = registrar_connector_manager.get_connector_instance(connector_name=connector_name)
            connector.update_prices(tld_name=tld_name)
        else:
            for connector_name in registrar_connector_manager.connectors_info:
                connector = registrar_connector_manager.get_connector_instance(connector_name=connector_name)
                connector.update_prices(tld_name=tld_name)
        return Response({'detail': _('Prices updated')})
