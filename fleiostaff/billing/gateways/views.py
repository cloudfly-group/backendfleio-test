import logging

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, filters, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from fleio.billing.gateways import exceptions as gateway_exceptions
from fleio.billing.gateways.utils import update_gateways_table
from fleio.billing.models import Gateway

from fleio.core.drf import StaffOnly
from fleio.core.utils import fleio_join_url

from .serializers import StaffGatewaySerializer, StaffRetrieveGatewaySerializer

LOG = logging.getLogger(__name__)


class ModuleSettingsJson(serializers.JSONField):
    def get_attribute(self, instance):
        gw_module = getattr(instance, 'module', None)
        if not gw_module:
            self.context['definition'] = {}
        else:
            self.context['definition'] = getattr(gw_module, 'settings', None)
        return super(ModuleSettingsJson, self).get_attribute(instance=instance)

    def to_representation(self, value):
        value = super(ModuleSettingsJson, self).to_representation(value)
        if self.context.get('definition', None) is None:
            return None
        return value

    def to_internal_value(self, data):
        data = super(ModuleSettingsJson, self).to_internal_value(data=data)
        new_data = {f['name']: f['value'] for f in data}
        return new_data


class GatewaysViewset(viewsets.ModelViewSet):
    serializer_class = StaffGatewaySerializer
    model = Gateway
    queryset = Gateway.objects.all()
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('display_name', )
    ordering_fields = ('id', 'display_name', 'enabled', 'visible_to_user', 'fixed_fee', 'percent_fee')
    search_fields = ('id', 'display_name')
    ordering = ['-enabled']
    http_method_names = ('get', 'put', 'patch')
    serializer_map = {
        'retrieve': StaffRetrieveGatewaySerializer
    }

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        update_gateways_table()
        return super().list(request, args, kwargs)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes((StaffOnly, ))
def staff_action(request, gateway, action_name):
    gw_not_available_msg = _('Gateway not available')
    # Get the gateway from database
    try:
        gateway_model = Gateway.objects.visible_to_staff().get(name=gateway)
    except Gateway.DoesNotExist:
        LOG.debug('Requested gateway is not available: {}'.format(gateway))
        raise exceptions.NotFound(detail=gw_not_available_msg)
    except Gateway.MultipleObjectsReturned:
        LOG.error('Multiple gateways found for {}'.format(gateway))
        raise exceptions.NotFound(detail=gw_not_available_msg)
    # Get the gateway module
    gw_module = getattr(gateway_model, 'module', None)
    if gw_module is None:
        raise exceptions.NotFound(detail=gw_not_available_msg)
    # Get the module action
    act_call = getattr(gw_module, action_name, None)
    if act_call is None or not callable(act_call) or getattr(act_call, 'staff_action', None) is not True:
        raise exceptions.NotFound()
    # Check for action allowed methods
    allowed_methods = getattr(act_call, 'allowed_methods', [])
    if request.method.lower() not in allowed_methods:
        raise exceptions.MethodNotAllowed(method=request.method)

    propagate_exception = hasattr(act_call, 'requires_redirect') and not getattr(act_call, 'requires_redirect')

    try:
        return act_call(request)
    except gateway_exceptions.InvoicePaymentException as e:
        LOG.exception(e)

        if propagate_exception:
            raise exceptions.APIException(e)

        redirect_url = fleio_join_url(settings.FRONTEND_URL, 'staff/billing/invoicing')
        if e.invoice_id:
            redirect_url = '{}/{}'.format(redirect_url, e.invoice_id)
        error_context = {'error_message': str(e),
                         'invoice_id': e.invoice_id,
                         'redirect_url': redirect_url}
        return render(request=request, template_name='gateways/generic_error.html', context=error_context)
    except Exception as e:
        LOG.exception(e)

        if propagate_exception:
            raise exceptions.APIException(e)

        invoice_id = request.query_params.get('invoice', '')
        redirect_url = fleio_join_url(settings.FRONTEND_URL, 'staff/billing/invoicing')
        if invoice_id:
            redirect_url = '{}/{}'.format(redirect_url, invoice_id)
        error_context = {'error_message': str(e),
                         'invoice_id': invoice_id,
                         'redirect_url': redirect_url}
        return render(request=request, template_name='gateways/generic_error.html', context=error_context)
