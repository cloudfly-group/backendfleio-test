import logging

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import ResellerOnly
from fleio.core.features import reseller_active_features
from fleio.core.models import Currency
from fleio.osbilling.models import ATTRIBUTE_UNITS
from fleio.osbilling.models import BillingResource
from fleio.osbilling.models import NUMBER_COMPARATORS
from fleio.osbilling.models import PricingPlan
from fleio.osbilling.models import PricingRule
from fleio.osbilling.models import STRING_COMPARATORS
from fleio.osbilling.models import TIME_UNITS
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.osbilling.metrics_display_information import METRICS_DISPLAY_NAME
from fleiostaff.osbilling.metrics_display_information import METRICS_HELP_TEXT
from fleiostaff.osbilling.views import RESOURCE_ATTRIBUTES_HELPERS
from reseller.osbilling.pricing.serializers.price_rule import ResellerPriceRuleSerializer

LOG = logging.getLogger(__name__)


class ResellerPriceRuleViewSet(viewsets.ModelViewSet):
    permission_classes = (ResellerOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)

    serializer_class = ResellerPriceRuleSerializer

    def get_queryset(self):
        queryset = PricingRule.objects.all()
        if not reseller_active_features.is_enabled('openstack.instances.traffic'):
            traffic_resource = BillingResource.objects.filter(name='instance_traffic').first()
            queryset = queryset.exclude(resource=traffic_resource).all()

        reseller_resources = user_reseller_resources(user=self.request.user)
        return queryset.filter(plan__reseller_resources=reseller_resources)

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
                if not reseller_active_features.is_enabled('openstack.instances.traffic'):
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
        return Response({
            'plans': plans,
            'resources': resources,
            'currencies': currencies,
            'time_units': self.choices_to_dict(TIME_UNITS),
            'attribute_units': self.choices_to_dict(ATTRIBUTE_UNITS),
            'number_operators': self.choices_to_dict(NUMBER_COMPARATORS),
            'string_operators': self.choices_to_dict(STRING_COMPARATORS)
        })

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
