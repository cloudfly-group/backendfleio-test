from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import TaxRule
from fleio.billing.taxrules.serializers import EndUserTaxRuleSerializer
from fleio.core.drf import EndUserOnly
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from fleio.core.exceptions import APIBadRequest
from fleio.core.models import Client


@api_view(['GET'])
@permission_classes([EndUserOnly])
def get_applicable_tax_rules(request: Request):
    client_id = request.query_params.get('client_id', None)
    if not client_id:
        raise APIBadRequest(_('No client id provided'))
    client = Client.objects.filter(id=client_id, users__in=[request.user]).first()
    if not client:
        raise APIBadRequest(_('No client found for provided id'))
    applicable_tax_rules = TaxRule.for_country_and_state(country=client.country_name, state=client.state)
    if len(applicable_tax_rules) == 0:
        return Response({})
    else:
        return Response(EndUserTaxRuleSerializer(instance=applicable_tax_rules, many=True).data)
