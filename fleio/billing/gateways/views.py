import logging

from django.conf import settings
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import throttling
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import throttle_classes
from rest_framework.response import Response

from fleio.billing.gateways import exceptions as gateway_exceptions
from fleio.billing.gateways.utils import get_recurring_payments_model_path
from fleio.billing.models import Gateway, RecurringPaymentsOrder
from fleio.billing.utils import get_payment_module_by_label
from fleio.core.drf import EndUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.utils import fleio_join_url

LOG = logging.getLogger(__name__)


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('id', 'name', 'instructions',)


class GatewaysViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Gateway.objects.visible_to_user()
    serializer_class = GatewaySerializer
    permission_classes = (EndUserOnly,)

    @action(detail=False, methods=['post'])
    def deactivate_recurring_payment_option(self, request, *args, **kwargs):
        del args, kwargs  # unused
        client = request.user.clients.all().first()
        if not client:
            raise APIBadRequest(_('No client is associated with your user.'))
        gateway_name = request.data.get('gateway_name')
        recurring_payments_model_path = get_recurring_payments_model_path(gateway_name=gateway_name)
        try:
            recurring_payments_model = import_string(recurring_payments_model_path)
        except ImportError:
            raise APIBadRequest(_('Could not find recurring payment options record for this gateway.'))
        recurring_payment_record = recurring_payments_model.objects.filter(client=client).first()
        if not recurring_payment_record:
            raise APIBadRequest(_('Could not find recurring payment options record for this gateway.'))
        recurring_payment_record.active = False
        recurring_payment_record.save()
        return Response({'detail': _('Ok')})

    @action(detail=False, methods=['post'])
    def reactivate_recurring_payment_option(self, request, *args, **kwargs):
        del args, kwargs  # unused
        client = request.user.clients.all().first()
        if not client:
            raise APIBadRequest(_('No client is associated with your user.'))
        gateway_name = request.data.get('gateway_name')
        recurring_payments_model_path = get_recurring_payments_model_path(gateway_name=gateway_name)
        try:
            recurring_payments_model = import_string(recurring_payments_model_path)
        except ImportError:
            raise APIBadRequest(_('Could not find recurring payment options record for this gateway.'))
        recurring_payment_record = recurring_payments_model.objects.filter(client=client).first()
        if not recurring_payment_record:
            raise APIBadRequest(_('Could not find recurring payment options record for this gateway.'))
        recurring_payment_record.active = True
        recurring_payment_record.save()
        return Response({'detail': _('Ok')})

    @action(detail=False, methods=['get'])
    def get_configured_recurring_payment_options(self, request, *args, **kwargs):
        del args, kwargs  # unused
        client = request.user.clients.all().first()
        if not client:
            raise APIBadRequest(_('No client to get recurring payment options for.'))
        gateways = Gateway.objects.visible_to_user()
        recurring_payments = []
        for gateway in gateways:
            recurring_payments_model_path = get_recurring_payments_model_path(gateway_name=gateway.name)
            try:
                recurring_payments_model = import_string(recurring_payments_model_path)
            except ImportError:
                LOG.info('Could not get recurring payments model for gateway {}'.format(gateway.name))
            else:
                recurring_payment_record = recurring_payments_model.objects.filter(client=client).first()
                ordering = RecurringPaymentsOrder.objects.filter(client=client, gateway_name=gateway.name).first()
                if recurring_payment_record:
                    recurring_payments.append({
                        'name': gateway.name,
                        'display_name': gateway.display_name,
                        'active': recurring_payment_record.active,
                        'order': ordering.order,
                    })
        return Response({'objects': sorted(recurring_payments, key=lambda k: k['order'])})

    @action(detail=False, methods=['post'])
    def change_recurrent_payments_order(self, request, *args, **kwargs):
        recurring_payment_gateway_name = request.data.get('recurring_payment_gateway_name', None)
        new_ordering = request.data.get('new_ordering')
        if not new_ordering:
            raise APIBadRequest(_('No new order to change the old one with'))
        client = request.user.clients.all().first()
        if not client:
            raise APIBadRequest(_('No client to get recurring payment options for.'))
        if not recurring_payment_gateway_name:
            raise APIBadRequest(_('Cannot change order for non existing recurring payments option.'))
        # get old recurring payment gateway order
        old_recurring_payment_gateway_related_order = RecurringPaymentsOrder.objects.filter(
            client=client,
            order=new_ordering,
        ).first()
        if not old_recurring_payment_gateway_related_order:
            raise APIBadRequest(_('Cannot change order with non existing recurring payments option.'))
        recurring_payment_gateway_related_order = RecurringPaymentsOrder.objects.filter(
            client=client,
            gateway_name=recurring_payment_gateway_name,
        ).first()
        if not recurring_payment_gateway_related_order:
            raise APIBadRequest(_('Cannot change order for non existing recurring payments option.'))
        # set the new orders we want
        # the new_ordering is one position lower (gets closer to one to be in the top of the list)
        recurring_payment_gateway_related_order.order = new_ordering
        recurring_payment_gateway_related_order.save()
        # move the other recurring payment gateway one position lower (farther than one)
        old_recurring_payment_gateway_related_order.order = (new_ordering + 1)
        old_recurring_payment_gateway_related_order.save()
        return Response({'detail': _('Ok')})


class CallbackRateThrottle(throttling.AnonRateThrottle):
    scope = 'gateway_callback'


@api_view(http_method_names=['GET', 'POST'])
@permission_classes((permissions.AllowAny, ))
@throttle_classes((CallbackRateThrottle, ))
def callback(request, gateway):
    generic_error_message = _('Callback error')
    # NOTE(tomo): checks that the gateway app exists
    try:
        gateway_app_conf = get_payment_module_by_label(mod_label=gateway)
    except Exception as e:
        LOG.exception(e)
        raise exceptions.ValidationError(detail=generic_error_message)
    else:
        if gateway_app_conf is None:
            raise exceptions.NotFound()
    # NOTE(tomo): checks that the gateway was configured (exists in database)
    try:
        gateway_model = Gateway.objects.enabled().get(name=gateway)
    except Gateway.DoesNotExist:
        LOG.error('Invalid callback for missing gateway: {}'.format(gateway))
        raise exceptions.NotFound()
    except Gateway.MultipleObjectsReturned:
        LOG.critical('Multiple gateways found for: {}'.format(gateway))
        raise exceptions.ValidationError(detail=generic_error_message)
    except Exception as e:
        LOG.critical('Unable to retrieve gateway {}: {}'.format(gateway, e))
        raise exceptions.ValidationError(detail=generic_error_message)
    # NOTE(tomo): initiate the gateway payment callback
    module_callback = getattr(gateway_model.module, 'callback', None)
    if not callable(module_callback):
        raise exceptions.NotFound()
    try:
        return module_callback(request)
    except exceptions.APIException:
        raise
    except gateway_exceptions.InvoicePaymentException as e:
        LOG.exception(e)
        if request.user and request.user.is_authenticated:
            # If this is an authenticated user, show a proper error message (ROMCARD leads to this)
            redirect_url = fleio_join_url(settings.FRONTEND_URL, 'billing/invoices')
            if e.invoice_id:
                redirect_url = '{}/{}'.format(redirect_url, e.invoice_id)
            error_context = {'error_message': _('Unable to continue due to a gateway error'),
                             'invoice_id': e.invoice_id,
                             'redirect_url': redirect_url}
            return render(request=request, template_name='gateways/generic_error.html', context=error_context)
        else:
            raise exceptions.ValidationError(detail=generic_error_message)
    except Exception as e:
        LOG.exception(e)
        raise exceptions.ValidationError(detail=generic_error_message)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes((EndUserOnly, ))
def action(request, gateway, action_name):
    gw_not_available_msg = _('Gateway not available')
    act_not_available_msg = _('Action not available')
    unable_to_continue_msg = _('Unable to continue due to an error. Please contact support')
    # Get the gateway from database
    try:
        gateway_model = Gateway.objects.visible_to_user().get(name=gateway)
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
    if act_call is None or not callable(act_call) or getattr(act_call, 'action', None) is not True:
        raise exceptions.NotFound(detail=act_not_available_msg)
    # Check for action allowed methods
    allowed_methods = getattr(act_call, 'allowed_methods', [])
    if request.method.lower() not in allowed_methods:
        raise exceptions.MethodNotAllowed(method=request.method)

    try:
        return act_call(request)
    except gateway_exceptions.InvoicePaymentException as e:
        LOG.error(e)
        redirect_url = fleio_join_url(settings.FRONTEND_URL, 'billing/invoices')
        if e.invoice_id:
            redirect_url = '{}/{}'.format(redirect_url, e.invoice_id)
        error_context = {'error_message': str(e),
                         'invoice_id': e.invoice_id,
                         'redirect_url': redirect_url}
        return render(request=request, template_name='gateways/generic_error.html', context=error_context)
    except Exception as e:
        LOG.error(e)
        invoice_id = request.query_params.get('invoice', '')
        redirect_url = fleio_join_url(settings.FRONTEND_URL, 'billing/invoices')
        if invoice_id:
            redirect_url = '{}/{}'.format(redirect_url, invoice_id)
        error_context = {
            'error_message': (
                unable_to_continue_msg if type(e) is not gateway_exceptions.GatewayException else str(e)
            ),
            'invoice_id': invoice_id,
            'redirect_url': redirect_url
        }
        return render(request=request, template_name='gateways/generic_error.html', context=error_context)
