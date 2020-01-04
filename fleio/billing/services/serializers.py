import logging

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from fleio.billing.cart.serializers import ItemConfigurableOptionSerializer
from fleio.billing.cart.serializers import ProductConfigOptionSerializer
from fleio.billing.models import Invoice
from fleio.billing.models import OrderItemTypes
from fleio.billing.models import Product
from fleio.billing.models import ProductCycle
from fleio.billing.models import Service
from fleio.billing.models import ServiceConfigurableOption
from fleio.billing.models.configurable_option import ConfigurableOptionStatus
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.serializers import CancellationRequestBriefSerializer
from fleio.billing.products.serializers import ProductBriefSerializer
from fleio.billing.products.serializers import ProductCycleBriefSerializer
from fleio.billing.settings import ServiceStatus

LOG = logging.getLogger(__name__)


class ServiceProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description')


class ServiceCycleBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCycle
        fields = ('id', 'name', 'display_name', 'fixed_price', 'currency')


class ServiceConfigurableOptionsSerializer(serializers.ModelSerializer):
    display = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = ServiceConfigurableOption
        fields = ('display', 'has_price', 'price', 'quantity', 'option_value', 'taxable', 'unit_price')


class ServiceBriefSerializer(serializers.ModelSerializer):
    product = ProductBriefSerializer(read_only=True)
    cycle = ProductCycleBriefSerializer(read_only=True)
    cancellation_request = CancellationRequestBriefSerializer(read_only=True)
    configurable_options = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    pricing_plan = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ('id', 'display_name', 'status', 'suspend_type', 'created_at', 'activated_at',
                  'updated_at', 'terminated_at', 'auto_terminate_date', 'auto_terminate_reason',
                  'next_due_date', 'next_expiration_date', 'next_invoice_date', 'product', 'cycle',
                  'override_price', 'cancellation_request', 'configurable_options', 'status_display',
                  'domain_name', 'pricing_plan')
        read_only_fields = fields

    @staticmethod
    def get_pricing_plan(service):
        if getattr(service, 'service_dynamic_usage', None):
            return {
                'id': service.service_dynamic_usage.plan.id,
                'name': service.service_dynamic_usage.plan.name
            }
        return None

    @staticmethod
    def get_configurable_options(obj):
        visible_options = obj.configurable_options.visible_to_client()
        return ServiceConfigurableOptionsSerializer(read_only=True,
                                                    many=True).to_representation(visible_options)

    @staticmethod
    def get_status_display(service):
        return ServiceStatus.status_map.get(service.status, _('n/a'))


class ProductUpgradesCyclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCycle
        fields = ('id', 'display_name', 'fixed_price', 'currency')


class ProductUpgradesSerializer(serializers.ModelSerializer):
    """Serialize a list of products with cycles"""
    cycles = serializers.SerializerMethodField()
    configurable_options = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cycles', 'configurable_options')

    def get_cycles(self, product: Product):
        currency = self.context.get('currency')
        if not currency:
            raise serializers.ValidationError(_('Unable to determine currency'))
        cycles_qs = product.cycles.filter(currency=currency)
        return ProductUpgradesCyclesSerializer(many=True).to_representation(cycles_qs)

    def get_configurable_options(self, obj):
        service = self.context.get('service')
        if service:
            cycle = service.cycle
        else:
            cycle = None
        if cycle:
            cycle_name = cycle.cycle
            cycle_multiplier = cycle.cycle_multiplier
            cycle_currency = cycle.currency.code
            public_opts_with_cycles = obj.configurable_options.public().with_cycles(cycle=cycle_name,
                                                                                    cycle_multiplier=cycle_multiplier,
                                                                                    currency=cycle_currency)
            return ProductConfigOptionSerializer(many=True,
                                                 read_only=True,
                                                 context={'cycle': cycle}).to_representation(public_opts_with_cycles)
        else:
            # NOTE(tomo): No cycle, no configurable options
            return []


class ServiceConfigurableOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConfigurableOption
        fields = '__all__'


class ServiceConfigOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConfigurableOption
        fields = '__all__'


class ServiceUpgOptionsSerializer(serializers.Serializer):
    invalid_product_msg = _('Invalid product selected')
    invalid_cycle_msg = _('Invalid product cycle selected')
    product = serializers.PrimaryKeyRelatedField(write_only=True,
                                                 queryset=Product.objects.available_for_order(),
                                                 error_messages={'does_not_exist': invalid_product_msg,
                                                                 'incorrect_type': invalid_product_msg})
    cycle = serializers.PrimaryKeyRelatedField(write_only=True,
                                               queryset=ProductCycle.objects.available_for_order(),
                                               error_messages={'does_not_exist': invalid_cycle_msg,
                                                               'incorrect_type': invalid_cycle_msg})
    configurable_options = ItemConfigurableOptionSerializer(many=True, required=False)

    confirm = serializers.BooleanField(default=False)
    # configurable_options = ServiceConfigOptionSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super(ServiceUpgOptionsSerializer, self).__init__(*args, **kwargs)
        assert 'service' in self.context, 'Serializer {} needs Service model in context'.format(self.__class__.__name__)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        attrs = super(ServiceUpgOptionsSerializer, self).validate(attrs)
        service = self.context.get('service')

        # Validate no pending orders exist for this service
        existing_invoices = Invoice.objects.filter(items__item_type=OrderItemTypes.serviceUpgrade,
                                                   items__service=service,
                                                   status=InvoiceStatus.ST_UNPAID).count()
        if existing_invoices > 0:
            raise serializers.ValidationError(detail=_('An upgrade/downgrade invoice already exists for this service'))

        # Validate product and cycle exist and match
        product = attrs['product']
        cycle = attrs['cycle']
        if product == service.product:
            # Cycle or options upgrade only since this is the same product
            new_product = product
        else:
            try:
                new_product = service.product.upgrades.get(pk=product.pk)
            except (Product.DoesNotExist, AttributeError) as e:
                LOG.exception(e)
                raise serializers.ValidationError(detail=_('Unable to upgrade to the selected product'))
        try:
            new_product.cycles.get(pk=cycle.pk)
        except (ProductCycle.DoesNotExist, AttributeError):
            raise serializers.ValidationError(detail=_('Unable to upgrade to the selected product and cycle'))

        # validate configurable options are valid and public and all required are present
        configurable_options = attrs.get('configurable_options', [])
        if cycle and configurable_options:
            req_filter = dict(cycle=cycle.cycle,
                              cycle_multiplier=cycle.cycle_multiplier,
                              currency=cycle.currency,
                              required=True)
            required_options = product.configurable_options.public().with_cycles(**req_filter)
            for req_opt in required_options:
                found = False
                for sent_opt in configurable_options:
                    if req_opt.pk == sent_opt['option'].pk:
                        found = True
                if not found:
                    raise serializers.ValidationError(
                        detail=_('Value is required for {}').format(req_opt.description))
        for conf_opt in configurable_options:
            db_opt = conf_opt.get('option')
            if not db_opt:
                raise serializers.ValidationError(detail=_('Invalid option selected'))
            if db_opt.status != ConfigurableOptionStatus.public:
                raise serializers.ValidationError(detail=_('Invalid option selected'))
            # if not product.configurable_options.filter(id=db_opt.id).exists():
            #    raise serializers.ValidationError(detail=_('Invalid option selected'))

        return attrs


class ServiceChangeOptionsSerializer(serializers.ModelSerializer):
    upgrades = serializers.SerializerMethodField()
    cycle_upgrades = serializers.SerializerMethodField()
    configurable_options_upgrades = serializers.SerializerMethodField()
    product = ServiceProductBriefSerializer(read_only=True)
    cycle = ServiceCycleBriefSerializer(read_only=True)
    existing_upgrade_invoice = serializers.SerializerMethodField()
    configurable_options = ItemConfigurableOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'display_name', 'cycle', 'status', 'upgrades', 'existing_upgrade_invoice',
                  'cycle_upgrades', 'product', 'configurable_options', 'configurable_options_upgrades')
        read_only_fields = ('display_name', 'cycle', 'status', 'task')

    @staticmethod
    def get_upgrades(service: Service):
        currency = service.client.currency
        qs = service.product.upgrades_with_cycles(currency=currency)
        return ProductUpgradesSerializer(many=True, context={'currency': currency,
                                                             'service': service}).to_representation(qs)

    @staticmethod
    def get_cycle_upgrades(service: Service):
        currency = service.client.currency
        qs = service.product.cycles.available_for_order(currency=currency)
        if service.cycle_id:
            qs = qs.exclude(pk=service.cycle_id)
        qs = qs.distinct()
        return ProductUpgradesCyclesSerializer(many=True).to_representation(qs)

    @staticmethod
    def get_configurable_options_upgrades(service: Service):
        cycle = service.cycle
        prod = service.product
        if cycle:
            cycle_name = cycle.cycle
            cycle_multiplier = cycle.cycle_multiplier
            cycle_currency = cycle.currency.code
            public_opts_with_cycles = prod.configurable_options.public().with_cycles(cycle=cycle_name,
                                                                                     cycle_multiplier=cycle_multiplier,
                                                                                     currency=cycle_currency)
            return ProductConfigOptionSerializer(many=True,
                                                 read_only=True,
                                                 context={'cycle': cycle}).to_representation(public_opts_with_cycles)
        else:
            # NOTE(tomo): No cycle, no configurable options
            return []

    @staticmethod
    def get_existing_upgrade_invoice(service: Service):
        """Get existing pending upgrade orders"""
        existing_invoice = Invoice.objects.filter(items__item_type=OrderItemTypes.serviceUpgrade,
                                                  items__service=service,
                                                  status=InvoiceStatus.ST_UNPAID).distinct().first()
        if existing_invoice:
            return existing_invoice.pk
        else:
            return None


class StaffCreateServiceSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_cycle_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
