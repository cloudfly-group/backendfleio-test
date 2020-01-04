import logging
import decimal

from rest_framework.exceptions import ValidationError
from uuid import uuid4

from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from fleio.billing.models import ConfigurableOption, ConfigurableOptionChoice, FleioCart, OrderItem, ProductCycle
from fleio.billing.models import Product
from fleio.billing.models.configurable_option import ConfigurableOptionCycle, ConfigurableOptionStatus
from fleio.billing.models.order_item_configurable_option import OrderItemConfigurableOption
from fleio.billing.orders.utils import OrderMetadata
from fleio.billing.settings import PricingModel
from fleio.core.models import get_default_currency
from fleio.core.plugins.plugin_utils import PluginUtils
from .utils import get_order_item_prices
from .utils import get_client_taxes_amount_by_price

LOG = logging.getLogger(__name__)

CART_SESSION_KEY = 'fleio_cart_id'


def create_cart(request) -> FleioCart:
    cart_session_id = str(uuid4())
    cart_data = {}
    cart_metadata = OrderMetadata.from_request(request).to_json()
    if request.user.is_authenticated:
        cart_data['user'] = request.user.pk
        user_client = request.user.clients.first()
        if user_client:
            cart_data['client'] = user_client.pk
            cart_data['currency'] = user_client.currency.code

    if cart_data.get('currency') is None:
        cart_data['currency'] = get_default_currency().code
    cart_serializer = CartSerializer(data=cart_data)
    cart_serializer.is_valid(raise_exception=True)
    cart = cart_serializer.save(metadata=cart_metadata, storage_id=cart_session_id)
    request.session[CART_SESSION_KEY] = cart_session_id
    return cart


def cart_from_request(request, create=False) -> FleioCart:
    cart_session_id = request.session.get(CART_SESSION_KEY)
    if request.user.is_authenticated:
        """Get the current user cart by user or by id in session"""
        db_cart = FleioCart.objects.filter(user=request.user).first()
        if db_cart is None:
            # User has no current or previous cart assigned, check by id (happens after logging in)
            if cart_session_id:
                db_cart = FleioCart.objects.filter(storage_id=cart_session_id, user__isnull=True).first()
            if db_cart is None:
                # Still no cart, create a new one or return None
                if create:
                    return create_cart(request=request)
            else:
                """Cart exists by id, update user and client"""
                db_cart.user = request.user
                db_cart.client = request.user.clients.first()
                db_cart.metadata = OrderMetadata.from_request(request).to_json()
                db_cart.save(update_fields=('user', 'client', 'metadata'))
        return db_cart
    else:
        db_cart = None
        if cart_session_id:
            # If the user was previously authenticated, this will hide the cart once he goes anonymous
            db_cart = FleioCart.objects.filter(storage_id=cart_session_id, user__isnull=True).first()
        if db_cart is None and create:
            db_cart = create_cart(request=request)
        return db_cart


class ProductCycleSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = ProductCycle
        fields = ('id', 'display_name', 'fixed_price', 'setup_fee', 'currency')


class QuantityWidgetSettingsSerializer(serializers.Serializer):
    min = serializers.IntegerField(required=False)
    max = serializers.IntegerField(required=False)
    step = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ItemConfigurableOptionSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=255, source='option.description', read_only=True)
    display = serializers.SerializerMethodField()
    is_free = serializers.BooleanField(read_only=True)

    class Meta:
        model = OrderItemConfigurableOption
        read_only_fields = ('id', 'quantity', 'has_price', 'price', 'setup_fee',
                            'order_item', 'display', 'description', 'unit_price', 'is_free')
        fields = read_only_fields + ('option_value', 'option',)

    def validate(self, attrs):
        attrs = super(ItemConfigurableOptionSerializer, self).validate(attrs)
        option_value = attrs.get('option_value')
        config_option = attrs.get('option')
        attrs['quantity'] = 1
        if config_option.has_choices and not config_option.choices.filter(choice=option_value).exists():
            # NOTE(tomo): Validate a valid choice has been entered
            raise serializers.ValidationError(detail=_('Option not available'))
        elif config_option.has_quantity:
            # NOTE(tomo): Validate a valid quantity has been entered
            try:
                attrs['option_value'] = option_value = int(option_value)
            except (TypeError, ValueError):
                raise serializers.ValidationError(detail=_('Invalid value provided'))
            if option_value < 0:
                raise serializers.ValidationError(detail=_('Value must be greater or equal to 0'))
            attrs['quantity'] = option_value
        self.settings_validation(config_option=config_option, value=option_value)
        return attrs

    @staticmethod
    def settings_validation(config_option: ConfigurableOption, value):
        settings = config_option.settings
        if config_option.widget == 'num_in':
            conf_settings = QuantityWidgetSettingsSerializer(data=settings)
            if conf_settings.is_valid(raise_exception=False):
                min_setting = conf_settings.validated_data.get('min')
                max_setting = conf_settings.validated_data.get('max')
                step_setting = conf_settings.validated_data.get('step')
                if min_setting is not None and value < min_setting:
                    raise serializers.ValidationError(detail='Value is lower than minimum')
                if max_setting is not None and value > max_setting:
                    raise serializers.ValidationError(detail='Value is higher than maximum')
                if step_setting is not None and step_setting != 0:
                    if value % step_setting != 0:
                        raise serializers.ValidationError(detail='Invalid value provided')

    def to_representation(self, instance):
        representation = super(ItemConfigurableOptionSerializer, self).to_representation(instance=instance)
        if instance.option.has_quantity:
            try:
                representation['option_value'] = int(representation['option_value'])
            except ValueError:
                representation['option_value'] = 0
        return representation

    @staticmethod
    def get_display(obj):
        if not obj.option:
            return 'Option'
        if obj.option.has_choices:
            choice = obj.option.choices.filter(choice=obj.option_value).first()
            if choice and choice.label:
                return '{}: {}'.format(obj.option.description, choice.label)
            else:
                return '{}: {}'.format(obj.option.description, choice.choice)
        elif obj.option.has_quantity:
            return '{}: {}'.format(obj.option.description, obj.quantity)
        elif obj.option.widget == 'yesno':
            return '{}'.format(obj.option.description)
        else:
            return '{}: {}'.format(obj.option.description, obj.option_value)


class OrderTaxesSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    tax_name = serializers.CharField(source='taxes__name', max_length=128, read_only=True)

    class Meta:
        fields = '__all__'

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ConfigOptionCycleSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)
    free = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurableOptionCycle
        fields = ('id', 'display_name', 'price', 'setup_fee', 'currency', 'free')

    @staticmethod
    def get_free(obj):
        return obj.price == obj.setup_fee == decimal.Decimal('0.00')


class ConfigOptionChoiceSerializer(serializers.ModelSerializer):
    cycle = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurableOptionChoice
        fields = '__all__'

    def get_cycle(self, obj):
        cycle = self.context.get('cycle')
        if not cycle:
            return None

        cycle_choice = obj.cycles.filter(cycle=cycle.cycle,
                                         cycle_multiplier=cycle.cycle_multiplier,
                                         currency=cycle.currency).first()
        if cycle_choice is None:
            return None
        return ConfigOptionCycleSerializer(read_only=True).to_representation(cycle_choice)


class ProductConfigOptionSerializer(serializers.ModelSerializer):
    settings = serializers.JSONField(read_only=True)
    choices = serializers.SerializerMethodField()
    cycle = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurableOption
        fields = ('id', 'name', 'description', 'widget', 'settings', 'choices', 'cycle', 'required')

    def get_choices(self, obj):
        cycle = self.context.get('cycle')
        if cycle:
            choices_with_cycles = obj.choices.filter(cycles__cycle=cycle.cycle,
                                                     cycles__cycle_multiplier=cycle.cycle_multiplier,
                                                     cycles__currency=cycle.currency)
            return ConfigOptionChoiceSerializer(read_only=True,
                                                many=True,
                                                context={'cycle': cycle}).to_representation(choices_with_cycles)
        else:
            return ConfigOptionChoiceSerializer(read_only=True, many=True).to_representation(obj.choices.all())

    def get_cycle(self, obj):
        cycle = self.context.get('cycle')
        if not cycle:
            return None
        if cycle:
            cycles_matched = obj.cycles.filter(cycle=cycle.cycle,
                                               cycle_multiplier=cycle.cycle_multiplier,
                                               currency=cycle.currency).first()
            if not cycles_matched:
                return None
            return ConfigOptionCycleSerializer(read_only=True,
                                               context={'cycle': cycle}).to_representation(cycles_matched)


class CartProductCreateOptionsSerializer(serializers.ModelSerializer):
    """Serializer for create and edit options for a cart item"""
    selected_cycle = serializers.SerializerMethodField()
    cycles = serializers.SerializerMethodField()
    has_plugin = serializers.SerializerMethodField()
    plugin_label = serializers.SerializerMethodField()
    configurable_options = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'cycles', 'has_plugin', 'plugin_label', 'configurable_options',
            'name', 'description', 'code', 'has_quantity', 'available_quantity',
            'selected_cycle', 'requires_domain',
        )

    @staticmethod
    def get_has_plugin(obj):
        return PluginUtils.has_enduser_component(plugin_label=obj.module.plugin_label,
                                                 component_name='OrderProduct')

    def get_cycles(self, obj):
        """Return only cycles that match the cart currency for the selected product"""
        cart = self.context.get('cart')
        if not cart:
            LOG.error('No cart set for serializer {}'.format(self.__name__))
            raise serializers.ValidationError(detail=_('Invalid request'))
        else:
            request_currency = cart.currency
        cycles = obj.cycles.available_for_order(currency=request_currency)
        return ProductCycleSerializer(read_only=True, many=True).to_representation(cycles)

    @staticmethod
    def get_plugin_label(obj):
        return obj.module.plugin_label

    def get_public_cycle(self, obj):
        del obj  # unused
        return self.context.get('cycle')

    def get_selected_cycle(self, obj):
        cycle = self.get_public_cycle(obj)
        return cycle.id if cycle else None

    def get_configurable_options(self, obj):
        cycle = self.get_public_cycle(obj)
        if cycle:
            cycle_name = cycle.cycle
            cycle_multiplier = cycle.cycle_multiplier
            cycle_currency = cycle.currency.code
            public_opts_with_cycles = obj.configurable_options.public().with_cycles(cycle=cycle_name,
                                                                                    cycle_multiplier=cycle_multiplier,
                                                                                    currency=cycle_currency)
            return ProductConfigOptionSerializer(
                many=True,
                read_only=True,
                context={'cycle': cycle}
            ).to_representation(
                [opt for opt in public_opts_with_cycles.all() if opt.product_cycles_match(product=obj)]
            )
        else:
            # NOTE(tomo): No cycle, no configurable options
            return []


class OrderItemCreateOptionsSerializer(serializers.Serializer):
    """Validates the query parameters for cart item create options"""
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.available_for_order(),
                                                 required=False,
                                                 error_messages={'does_not_exist': _('Product not found'),
                                                                 'incorrect_type': _('Product not found')})
    product_code = serializers.SlugRelatedField(queryset=Product.objects.available_for_order(),
                                                required=False,
                                                slug_field='code',
                                                error_messages={'does_not_exist': _('Product not found'),
                                                                'invalid': _('Product not found')})
    cycle = serializers.PrimaryKeyRelatedField(queryset=ProductCycle.objects.available_for_order(),
                                               required=False,
                                               error_messages={'does_not_exist': _('Product cycle not found'),
                                                               'incorrect_type': _('Product cycle not found')})

    def get_currency_or_default(self):
        cart = self.context.get('cart')
        if not cart:
            LOG.error('No cart set for serializer {}'.format(self.__name__))
            raise serializers.ValidationError(detail=_('Invalid request'))
        return cart.currency

    def validate(self, attrs):
        currency = self.get_currency_or_default()
        product = attrs.get('product', attrs.pop('product_code', None))  # type: Product
        if product is None:
            raise serializers.ValidationError({'detail': _('Specify a product code or id')})
        attrs['product'] = product  # NOTE(tomo): avoid having either product or product_code.
        cycle = attrs.get('cycle')
        if product.price_model == PricingModel.free:
            attrs['cycle'] = None
        elif cycle:
            if not product.cycles.available_for_order(currency=currency).filter(pk=cycle.pk).exists():
                raise serializers.ValidationError({'detail': _('Product not available')})
        else:
            cycle = product.cycles.available_for_order(currency=currency).first()
            if cycle is None:
                raise serializers.ValidationError({'detail': _('Product not available')})
            else:
                attrs['cycle'] = cycle
        return attrs

    def update(self, instance, validated_data):
        raise serializers.ValidationError(detail='Unable to create')

    def create(self, validated_data):
        raise serializers.ValidationError(detail='Unable to update')


class CurrentCartDefault:
    """Serializer validator for default field"""

    def __init__(self, *args, **kwargs):
        del args, kwargs  # unused
        self.cart = None

    def set_context(self, serializer_field):
        request = serializer_field.context.get('request')
        if request:
            current_cart = cart_from_request(request=request, create=True)
            if current_cart is not None:
                self.cart = current_cart

    def __call__(self):
        return self.cart


class OrderItemSerializer(serializers.ModelSerializer):
    cart = serializers.HiddenField(default=CurrentCartDefault())
    item_type = serializers.HiddenField(default='service')
    taxable = serializers.HiddenField(default=False)
    taxes = serializers.HiddenField(default=[])
    quantity = serializers.HiddenField(default=1)  # FIXME(tomo): Add quantity support, see issue 1269
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    fixed_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    setup_fee = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    setup_fees_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    has_plugin = serializers.SerializerMethodField()
    plugin_label = serializers.SerializerMethodField()
    plugin_data = serializers.JSONField(default={})
    configurable_options = ItemConfigurableOptionSerializer(many=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.available_for_order(),
        error_messages={
            'does_not_exist': _('Product not found'),
            'incorrect_type': _('Product not found')
        },
    )
    domain_name = serializers.CharField(max_length=256, default=None, allow_blank=True, allow_null=True)
    domain_action = serializers.CharField(max_length=64, default=None, allow_blank=True, allow_null=True)

    class Meta:
        model = OrderItem
        exclude = ('service', 'order')
        read_only_fields = ('currency', 'item_type', 'name', 'description',
                            'cycle_display', 'created_at', 'updated_at', 'quantity',
                            'amount')

    @staticmethod
    def update_pricing_from_product(attrs):
        """Order prices are setup here"""
        cart = attrs['cart']
        product = attrs['product']
        cycle = attrs.get('cycle')
        quantity = attrs.get('quantity')
        attrs['fixed_price'], attrs['setup_fee'], attrs['taxable'] = get_order_item_prices(cart=cart,
                                                                                           product=product,
                                                                                           quantity=quantity,
                                                                                           cycle=cycle)

    def validate(self, attrs):
        cart = attrs['cart']
        product = attrs.get('product')
        cycle = attrs.get('cycle')
        attrs['name'] = product.name
        attrs['description'] = product.description or product.name or 'Product'  # NOTE(tomo): description is required
        if not cycle and product.price_model != PricingModel.free:
            raise serializers.ValidationError({'cycle': _('A billing cycle is required')})
        if cycle:
            try:
                product.cycles.available_for_order(currency=cart.currency).get(pk=cycle.pk)
            except (ProductCycle.DoesNotExist, ProductCycle.MultipleObjectsReturned):
                LOG.debug('Tried to add a product to cart with an invalid currency.'
                          ' Cart currency {}; Cycle currency: {}'.format(cart.currency, cycle.currency))
                raise serializers.ValidationError(detail=_('Product not available'))
            attrs['cycle_display'] = cycle.display_name

        # update pricing information here
        self.update_pricing_from_product(attrs=attrs)

        # validate configurable options are valid and public and all required are present
        configurable_options = attrs.get('configurable_options')
        if cycle:
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
                    raise serializers.ValidationError(detail=_('Value is required for {}').format(req_opt.description))

        for conf_opt in configurable_options:
            db_opt = conf_opt.get('option')
            if not db_opt:
                raise serializers.ValidationError(detail=_('Invalid option selected'))
            if db_opt.status != ConfigurableOptionStatus.public:
                raise serializers.ValidationError(detail=_('Invalid option selected'))
            if not product.configurable_options.filter(id=db_opt.id).exists():
                raise serializers.ValidationError(detail=_('Invalid option selected'))

        # validate plugin data
        plugin_label = product.module.plugin_label
        component = PluginUtils.get_enduser_component(
            plugin_label=plugin_label,
            component_name='OrderProduct',
        )

        if component:
            plugin_data = attrs['plugin_data']
            serializer = component.create_serializer(plugin_data=plugin_data, context=self.context)
            if serializer:
                try:
                    serializer.is_valid(raise_exception=True)
                except ValidationError as e:
                    raise ValidationError(detail={
                        'plugin_data': e.detail
                    })

        return super().validate(attrs)

    @staticmethod
    def get_has_plugin(obj):
        return PluginUtils.has_enduser_component(plugin_label=obj.product.module.plugin_label,
                                                 component_name='OrderProduct')

    @staticmethod
    def get_plugin_label(obj):
        return obj.product.module.plugin_label

    @staticmethod
    def create_taxes(order_item):
        """Add taxes to an order item"""
        cart = order_item.cart
        client = cart.client if cart.client else None
        if client is None:
            # Client required to get country and state for taxes but not available for anonymous
            return
        price = order_item.setup_fee + order_item.fixed_price
        for conf_opt in order_item.configurable_options.all():
            if conf_opt.taxable:
                price += conf_opt.price + conf_opt.setup_fee
        taxes = get_client_taxes_amount_by_price(price=price, client=client, taxable=order_item.taxable)
        for tax in taxes:
            order_item.taxes.create(name=tax['name'], amount=tax['amount'])

    def create(self, validated_data):
        configurable_options = validated_data.pop('configurable_options', None)
        with transaction.atomic():
            order_item = super(OrderItemSerializer, self).create(validated_data=validated_data)
            for config_option in configurable_options:
                choice_value = None
                has_price = True
                if config_option['option'].widget == 'text_in':
                    has_price = False
                if config_option['option'].widget == 'yesno':
                    if config_option['option_value'] != 'yes':
                        # Ignore unchecked checkboxes
                        continue
                quantity = config_option.get('quantity')
                if config_option['option'].has_choices:
                    choice_value = config_option['option_value']
                # filter out all configurable options that do not have the product cycles
                if not config_option['option'].has_cycle(
                        cycle=order_item.cycle.cycle,
                        cycle_multiplier=order_item.cycle.cycle_multiplier,
                        choice_value=choice_value,
                        currency=order_item.currency.code,
                ):
                    continue
                unit_price, price, setupfee = config_option['option'].get_price_by_cycle_quantity_and_choice(
                    cycle_name=order_item.cycle.cycle,
                    cycle_multiplier=order_item.cycle.cycle_multiplier,
                    currency=order_item.currency,
                    quantity=config_option['quantity'],
                    choice_value=choice_value,
                    option_value=config_option['option_value'],
                )
                order_item.configurable_options.create(option=config_option['option'],
                                                       option_value=config_option['option_value'],
                                                       quantity=quantity,
                                                       has_price=has_price,
                                                       taxable=validated_data['taxable'],
                                                       unit_price=unit_price,
                                                       price=price,
                                                       setup_fee=setupfee)
            self.create_taxes(order_item=order_item)

            return order_item

    def update(self, instance, validated_data):
        configurable_options = validated_data.pop('configurable_options', None)
        with transaction.atomic():
            # removing name and description from validated data since they should not be updated
            del validated_data['name'], validated_data['description']
            product = validated_data['product']
            component = PluginUtils.get_enduser_component(
                plugin_label=product.module.plugin_label,
                component_name='OrderProduct',
            )

            if component:
                plugin_data = validated_data['plugin_data']
                serializer = component.create_serializer(plugin_data=plugin_data, context=self.context)
                if serializer and serializer.is_valid(raise_exception=True):
                    # update data just in case it was changed during validation process
                    validated_data['plugin_data'] = dict(serializer.validated_data)
                    # TODO: this is a temporary solution, we should abstract this so it would not depend on domains
                    if product.module.plugin_label == 'domains':
                        validated_data['name'] = plugin_data['name']

            order_item = super().update(instance=instance, validated_data=validated_data)  # type: OrderItem
            order_item.configurable_options.all().delete()
            for config_option in configurable_options:
                # Filter out all configurable options no longer valid
                if not config_option['option'].has_cycle(
                        cycle=order_item.cycle.cycle,
                        cycle_multiplier=order_item.cycle.cycle_multiplier,
                        choice_value=config_option.get('option_value'),
                        currency=order_item.currency.code,
                ):
                    continue
                if config_option['option'].widget == 'yesno':
                    if config_option['option_value'] != 'yes':
                        # Ignore unchecked checkboxes
                        continue
                choice_value = None
                has_price = True
                if config_option['option'].widget == 'text_in':
                    has_price = False
                quantity = config_option.get('quantity')
                if config_option['option'].has_choices:
                    choice_value = config_option['option_value']
                unit_price, price, setupfee = config_option['option'].get_price_by_cycle_quantity_and_choice(
                    cycle_name=order_item.cycle.cycle,
                    cycle_multiplier=order_item.cycle.cycle_multiplier,
                    currency=order_item.currency,
                    quantity=config_option['quantity'],
                    choice_value=choice_value,
                    option_value=config_option['option_value'],
                )
                order_item.configurable_options.create(option=config_option['option'],
                                                       option_value=config_option['option_value'],
                                                       quantity=quantity,
                                                       has_price=has_price,
                                                       taxable=validated_data['taxable'],
                                                       unit_price=unit_price,
                                                       price=price,
                                                       setup_fee=setupfee)
            # Update order item taxes
            order_item.taxes.all().delete()
            self.create_taxes(order_item=order_item)

            return order_item


class CartSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    subtotal = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    taxes = OrderTaxesSerializer(many=True, read_only=True)
    setup_fees = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    created_at = serializers.HiddenField(default=None)
    storage_id = serializers.HiddenField(default=str(uuid4()))

    class Meta:
        model = FleioCart
        exclude = ('metadata',)
