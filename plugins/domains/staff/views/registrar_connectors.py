from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _

from fleio.core.drf import StaffOnly

from plugins.domains.models import RegistrarConnector
from plugins.domains.registrars_connectors.exceptions import RegistrarConnectorException
from plugins.domains.registrars_connectors.registrar_connector_manager import registrar_connector_manager
from plugins.domains.staff.serializers import RegistrarConnectorSerializer
from plugins.domains.staff.serializers import RegistrarConnectorWithPricesSerializer


class RegistrarConnectorsViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly, )
    queryset = RegistrarConnector.objects.all()
    serializer_class = RegistrarConnectorSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        registrar_connector_manager.register_connectors()

    @action(methods=['GET'], detail=False)
    def registrar_prices(self, request):
        ser = RegistrarConnectorWithPricesSerializer(context={'request': request}, many=True)
        data = ser.to_representation(RegistrarConnector.objects.exclude(class_name__exact='TODORegistrarConnector'))
        return Response(data)

    @action(methods=['POST'], detail=False)
    def update_registrar_prices(self, request):
        connector_name = request.data.get('connector')
        tld_name = request.data.get('tld_name')
        if connector_name:
            connector_info = registrar_connector_manager.connectors_info.get(connector_name, None)
            if not connector_info:
                raise ValidationError(detail=_('Connector {} not found').format(connector_name))
            connector = registrar_connector_manager.get_connector_instance(connector_name=connector_name)
            try:
                connector.update_prices(tld_name=tld_name)
            except RegistrarConnectorException as e:
                raise ValidationError(detail=str(e))
        else:
            for connector_name in registrar_connector_manager.connectors_info:
                connector = registrar_connector_manager.get_connector_instance(connector_name=connector_name)
                try:
                    connector.update_prices(tld_name=tld_name)
                except RegistrarConnectorException as e:
                    raise ValidationError(detail=str(e))
        return Response({'detail': _('Prices updated')})
