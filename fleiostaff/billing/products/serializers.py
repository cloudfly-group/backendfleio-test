from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.billing.models import Product
from fleio.billing.models import ProductCycle
from fleio.billing.models import ProductGroup
from fleio.billing.models import ProductModule
from fleio.billing.models import ConfigurableOption
from fleio.billing.models import ProductConfigurableOption
from fleio.billing.settings import PricingModel, ProductAutoSetup

from fleio.core.exceptions import APIBadRequest

from fleio.core.plugins.plugin_config_types import PluginConfigTypes
from fleio.core.plugins.plugin_utils import PluginUtils
from fleio.core.plugins.serialization import ComponentDataModelSerializer


class StaffProductCycleSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = ProductCycle
        fields = '__all__'


class StaffProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = '__all__'


class StaffProductModuleSerializer(serializers.ModelSerializer):
    config = serializers.JSONField(required=False)

    class Meta:
        model = ProductModule
        fields = '__all__'


class StaffProductSerializer(serializers.ModelSerializer):
    cycles = StaffProductCycleSerializer(many=True)
    module = StaffProductModuleSerializer()
    price_model_display = serializers.SerializerMethodField()
    auto_setup_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_price_model_display(product):
        try:
            return dict(PricingModel.choices)[product.price_model]
        except KeyError:
            return product.price_model

    @staticmethod
    def get_auto_setup_display(product):
        try:
            return dict(ProductAutoSetup.choices)[product.auto_setup]
        except KeyError:
            return product.auto_setup


class StaffProductGroupAllSerializer(serializers.ModelSerializer):
    products = StaffProductSerializer(many=True)

    class Meta:
        model = ProductGroup
        fields = '__all__'


class StaffProductConfigurableOptionSerializer(serializers.ModelSerializer):
    """Serializer that displays a product configurable option list"""
    cycles_match = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurableOption
        fields = '__all__'

    def get_cycles_match(self, obj):
        product = self.context.get('product')
        if product:
            return obj.product_cycles_match(product=product)
        else:
            return None


class StaffProductDetailSerializer(ComponentDataModelSerializer):
    cycles = StaffProductCycleSerializer(many=True)
    group = StaffProductGroupSerializer()
    module = StaffProductModuleSerializer()
    price_model_display = serializers.SerializerMethodField()
    auto_setup_display = serializers.SerializerMethodField()
    plugin_data = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        component_name = 'ProductSettings'
        plugin_config_type = PluginConfigTypes.staff

    @staticmethod
    def get_price_model_display(product):
        try:
            return dict(PricingModel.choices)[product.price_model]
        except KeyError:
            return product.price_model

    @staticmethod
    def get_auto_setup_display(product):
        try:
            return dict(ProductAutoSetup.choices)[product.auto_setup]
        except KeyError:
            return product.auto_setup

    @staticmethod
    def get_plugin_data(product):
        if product.module.plugin_label:
            component = PluginUtils.get_staff_component(
                plugin_label=product.module.plugin_label,
                component_name='ProductSettings'
            )

            if component:
                return component.get(product=product)

        return None


class StaffProductCreateSerializer(ComponentDataModelSerializer):
    id = serializers.CharField(read_only=True)
    plugin_data = serializers.JSONField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = '__all__'
        component_name = 'ProductSettings'
        plugin_config_type = PluginConfigTypes.staff


class StaffProductUpdateSerializer(ComponentDataModelSerializer):
    id = serializers.CharField(read_only=True)
    plugin_data = serializers.JSONField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = '__all__'
        component_name = 'ProductSettings'
        plugin_config_type = PluginConfigTypes.staff

    def save(self, **kwargs):
        with transaction.atomic():
            cycles_count = self.instance.cycles.count()
            if self.validated_data.get('price_model') == PricingModel.free and cycles_count > 0:
                raise APIBadRequest(_('Cannot make product free while it contains cycles.'))
            super().save(**kwargs)
            self.cleanup_component_data(keep_for_plugins=[self.instance.module.plugin])


class StaffAssociateConfigurableOption(serializers.ModelSerializer):
    class Meta:
        model = ProductConfigurableOption
        fields = '__all__'


class ProductUpgradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('upgrades', )
