import logging

import django_filters
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common_admin.osbilling.pricing.views.pricing_plan import AdminPricingPlanViewSet
from fleio.billing.modules.factory import module_factory
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.features import staff_active_features
from fleio.core.models import Client
from fleio.osbilling.models import ATTRIBUTE_UNITS
from fleio.osbilling.models import BillingResource
from fleio.osbilling.models import Currency
from fleio.osbilling.models import NUMBER_COMPARATORS
from fleio.osbilling.models import PricingPlan
from fleio.osbilling.models import PricingRule
from fleio.osbilling.models import PricingRuleCondition
from fleio.osbilling.models import PricingRuleModifier
from fleio.osbilling.models import STRING_COMPARATORS
from fleio.osbilling.models import ServiceDynamicUsage
from fleio.osbilling.models import ServiceDynamicUsageHistory
from fleio.osbilling.models import TIME_UNITS
from fleio.osbilling.serializers import ServiceDynamicUsageHistorySerializer
from fleio.osbilling.serializers import ServiceDynamicUsageSerializer
from fleio.reseller.utils import user_reseller_resources
from .metrics_display_information import METRICS_DISPLAY_NAME
from .metrics_display_information import METRICS_HELP_TEXT
from .resource import InstanceHelper
from .resource import InstanceTrafficHelper
from .resource import VolumeHelper
from .serializers import PriceRuleConditionSerializer
from .serializers import PriceRuleModifierSerializer
from .serializers import PriceRuleSerializer
from .serializers import PricingPlanUpdateSerializer
from .serializers import PricingPlanDeleteSerializer
from .serializers import PricingPlanSerializer
from .serializers import ResourceSerializer

LOG = logging.getLogger(__name__)

RESOURCE_ATTRIBUTES_HELPERS = (InstanceHelper, VolumeHelper, InstanceTrafficHelper)


class ResourceViewset(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('type', 'name')

    serializer_class = ResourceSerializer
    queryset = BillingResource.objects.all()


class PricingPlanViewset(AdminPricingPlanViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = PricingPlanSerializer
    serializer_map = {
        'destroy': PricingPlanDeleteSerializer,
        'update': PricingPlanUpdateSerializer,
    }


class PriceRuleViewset(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)

    serializer_class = PriceRuleSerializer
    queryset = PricingRule.objects.all()

    def get_queryset(self):
        if not staff_active_features.is_enabled('openstack.instances.traffic'):
            traffic_resource = BillingResource.objects.filter(name='instance_traffic').first()
            queryset = self.queryset.exclude(resource=traffic_resource).all()
            return queryset
        else:
            return self.queryset

    @staticmethod
    def choices_to_dict(choices):
        return {choice[0]: choice[1] for choice in choices if len(choices) > 1}

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        del request  # unused
        # Init attribute helpers
        attribute_helpers = dict()
        for attr_helper in RESOURCE_ATTRIBUTES_HELPERS:
            ah = attr_helper()
            if ah.type not in attribute_helpers:
                attribute_helpers[ah.type] = {ah.name: ah}
            else:
                attribute_helpers[ah.type][ah.name] = ah
        # Plans available for selection
        reseller_resources = user_reseller_resources(user=self.request.user)
        plans = PricingPlan.objects.for_reseller(reseller_resources=reseller_resources).values('name', 'id')
        # Resources, including attributes
        resources = list()
        for resource in BillingResource.objects.all():
            if resource.name == 'instance_traffic':
                # this resource type depends on a feature
                if not staff_active_features.is_enabled('openstack.instances.traffic'):
                    continue

            resource_display_name = resource.display_name or resource.name  # Display name is not required
            res_def = dict(name=resource_display_name, type=resource.type, id=resource.id)
            res_def['attributes'] = resource.attributes
            # Add metrics if present
            metrics_def = resource.definition.get('metrics', None)
            if metrics_def is not None:
                res_def['metrics'] = []
                for mtr in metrics_def:
                    res_def['metrics'].append(
                        {
                            'name': mtr.get('name', '- unnamed -'),
                            'help_text': METRICS_HELP_TEXT.get(mtr.get('name', ''), ''),
                            'display_name': METRICS_DISPLAY_NAME.get(
                                mtr.get('name', ''), mtr.get('name', '- unnamed -')
                            ),
                        }
                    )
            # Add attributes choices
            if resource.name in attribute_helpers.get(resource.type, dict()):
                try:
                    attribute_choices = attribute_helpers[resource.type][resource.name].get_attributes_choices()
                except Exception as e:
                    LOG.exception(e)
                else:
                    for res_attr in res_def['attributes']:
                        if res_attr['name'] in attribute_choices:
                            res_attr['choices'] = attribute_choices[res_attr['name']]

            # set display flags
            has_metrics = resource.type in ['metric', 'internal']
            res_def['metric_display'] = has_metrics
            res_def['attribute_display'] = not has_metrics

            resources.append(res_def)

        currencies = Currency.objects.all().values('code', 'is_default')
        return Response({'plans': plans,
                         'resources': resources,
                         'currencies': currencies,
                         'time_units': self.choices_to_dict(TIME_UNITS),
                         'attribute_units': self.choices_to_dict(ATTRIBUTE_UNITS),
                         'number_operators': self.choices_to_dict(NUMBER_COMPARATORS),
                         'string_operators': self.choices_to_dict(STRING_COMPARATORS)})

    @action(detail=True, methods=['post'])
    def validate_existing_rule(self, request, pk):
        del pk  # unused
        """Validate existing rule, called from frontend before saving"""
        price_rule = self.get_object()
        serializer = self.get_serializer(initial=price_rule, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'valid': True})

    @action(detail=False, methods=['post'])
    def validate_new_rule(self, request):
        """Validate new rule, called from frontend before saving"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'valid': True})


class PriceRuleConditionsViewset(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)

    serializer_class = PriceRuleConditionSerializer

    def get_queryset(self):
        return PricingRuleCondition.objects.filter(price_rule_id=self.kwargs['pricerule_pk'])

    def perform_create(self, serializer):
        serializer.save(price_rule_id=self.kwargs['pricerule_pk'])


class PriceRuleModifiersViewset(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)

    serializer_class = PriceRuleModifierSerializer

    def get_queryset(self):
        return PricingRuleModifier.objects.filter(price_rule_id=self.kwargs['pricerule_pk'])

    def perform_create(self, serializer):
        serializer.save(price_rule_id=self.kwargs['pricerule_pk'])


class StaffClientBillingViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = ServiceDynamicUsageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'start_date', 'end_date')

    def get_queryset(self):
        return ServiceDynamicUsage.objects.all()


class BillingHistoryFilter(django_filters.rest_framework.FilterSet):
    client = django_filters.CharFilter(field_name='service_dynamic_usage__service__client__id')
    external_billing_id = django_filters.CharFilter(
        field_name='service_dynamic_usage__service__client__external_billing_id'
    )

    class Meta:
        model = ServiceDynamicUsageHistory
        fields = ['id', 'start_date', 'end_date', 'client', 'external_billing_id', 'state']


class StaffClientBillingHistoryViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = ServiceDynamicUsageHistorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BillingHistoryFilter

    def get_queryset(self):
        billing_id = self.kwargs.get('billing_id', None)
        if billing_id:
            return ServiceDynamicUsageHistory.objects.filter(service_dynamic_usage=billing_id)
        else:
            return ServiceDynamicUsageHistory.objects.all()

    @action(detail=False, methods=['post'])
    def mark_billing_histories_as_invoiced(self, request):
        """Method called from external module (fleio-whmcs) to mark billing histories as invoiced"""
        client_external_billing_id = request.data.get('client_external_billing_id', None)
        if not client_external_billing_id:
            raise APIBadRequest(_('Client external billing id is required to fulfill this request.'))
        try:
            client = Client.objects.get(external_billing_id=client_external_billing_id)
        except Client.DoesNotExist:
            raise APIBadRequest(_('Could not find client related to given external billing id.'))
        for service in client.services.all():
            billing_module = module_factory.get_module_instance(service=service)
            # this will mark unsettled service dynamic usage histories to invoiced
            billing_module.get_unsettled_usage(service=service, end_datetime=utcnow())
        return Response({
            'detail': _('Successfully marked client {} billing histories states as invoiced.').format(client.id)
        })
