from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.billing.models import ConfigurableOption
from fleio.billing.models.configurable_option import ConfigurableOptionChoice
from fleio.billing.models.configurable_option import ConfigurableOptionCycle
from fleio.billing.models.configurable_option import ConfigurableOptionStatus
from fleio.billing.models.configurable_option import ConfigurableOptionWidget
from fleio.billing.settings import CyclePeriods
from fleio.core.drf import ResellerOnly
from fleio.core.models import Currency
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.billing.configurable_options.serializers import ConfigCycleSerializer
from fleiostaff.billing.configurable_options.serializers import ConfigurableOptionChoiceSerializer
from fleiostaff.billing.configurable_options.serializers import ConfigurableOptionsSerializer


class ResellerConfigurableOptionsViewSet(viewsets.ModelViewSet):
    permission_classes = (ResellerOnly, )
    serializer_class = ConfigurableOptionsSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name', 'products')
    search_fields = ('name', )
    ordering_fields = ('name', )

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return ConfigurableOption.objects.filter(visible=True, reseller_resources=reseller_resources).all()

    @action(methods=['GET'], detail=False)
    def create_options(self, request):
        del request  # unused
        widgets = [{'label': opt[1], 'value': opt[0]} for opt in ConfigurableOptionWidget.CHOICES]
        currencies = Currency.objects.all().values('code', 'is_default').order_by('code')
        default_currency = currencies.filter(is_default=True).first()
        return Response({'widgets': widgets,
                         'currencies': currencies,
                         'default_currency': default_currency,
                         'status_choices': ConfigurableOptionStatus.CHOICES,
                         'cycles': CyclePeriods.choices})


class ResellerConfigurableOptionsChoicesViewSet(viewsets.ModelViewSet):
    permission_classes = (ResellerOnly, )
    serializer_class = ConfigurableOptionChoiceSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('option',)
    queryset = ConfigurableOptionChoice.objects.all()

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return self.queryset.filter(option__reseller_resources=reseller_resources).all()


class ResellerConfigurableOptionsCyclesViewSet(viewsets.ModelViewSet):
    permission_classes = (ResellerOnly, )
    serializer_class = ConfigCycleSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('value', 'option')

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return ConfigurableOptionCycle.objects.filter(option__reseller_resources=reseller_resources).all()

    @action(methods=['GET'], detail=False)
    def create_options(self, request):
        del request  # unused
        cycles = [{'label': opt[1], 'value': opt[0]} for opt in CyclePeriods.choices]
        currencies = Currency.objects.all().values('code').order_by('code')
        default_currency = currencies.filter(is_default=True).first()
        return Response({'cycles': cycles,
                         'currencies': currencies,
                         'default_currency': default_currency})
