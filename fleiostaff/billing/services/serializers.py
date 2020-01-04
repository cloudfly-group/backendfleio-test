from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.billing.models import Invoice
from fleio.billing.models import Product
from fleio.billing.models import ProductCycle
from fleio.billing.models import Service
from fleio.billing.models import ServiceConfigurableOption
from fleio.billing.models import ServiceHostingAccount
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.utils import config_option_cycles_match_product
from fleio.core.clients.serializers import ClientWithExternalBillingMinSerializer
from fleio.servers.models import Server
from fleio.servers.models.server import ServerStatus


class StaffProductCycleBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCycle
        fields = ('id', 'display_name',)


class StaffProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description')


class StaffServiceConfigurableOptionsSerializer(serializers.ModelSerializer):
    display = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = ServiceConfigurableOption
        fields = '__all__'


class StaffHostingAccountSerializer(serializers.ModelSerializer):
    available_servers = serializers.SerializerMethodField()

    class Meta:
        model = ServiceHostingAccount
        fields = '__all__'
        read_only_fields = ('id', 'service',)

    @staticmethod
    def get_available_servers(hosting_account):
        try:
            plugin = hosting_account.service.product.module.plugin
        except ObjectDoesNotExist:
            return []
        servers = Server.objects.filter(status=ServerStatus.enabled,
                                        plugin__app_label=plugin.app_label).distinct()
        # Add max accounts
        servers = servers.annotate(num_accounts=Count('hosting_accounts'),
                                   max_accounts=F('hosting_server_settings__max_accounts'))
        # Filter out full servers (max accounts not reached or set to 0)
        servers = servers.filter(Q(num_accounts__lte=F('max_accounts')) | Q(max_accounts=0))
        servers = servers.order_by('created_at')
        if servers:
            return [{'id': server.id, 'name': server.name} for server in servers]
        else:
            return []


class StaffServiceSerializer(serializers.ModelSerializer):
    client = ClientWithExternalBillingMinSerializer(read_only=True)
    cycle = StaffProductCycleBriefSerializer(read_only=True)
    product = StaffProductBriefSerializer(read_only=True)
    order = serializers.SerializerMethodField()
    configurable_options = StaffServiceConfigurableOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

    @staticmethod
    def get_order(obj):
        db_obj = obj.order_item.values('order__id').first()
        return db_obj.get('order__id') if db_obj else None


class StaffServiceDetailsSerializer(StaffServiceSerializer):
    hosting_account = StaffHostingAccountSerializer()


class StaffServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('display_name', 'status', 'product', 'cycle', 'notes', 'override_price', 'override_suspend_until',
                  'next_due_date', 'next_expiration_date', 'next_invoice_date', 'suspend_reason', 'suspend_type',
                  'external_billing_id',)

    def update(self, instance, validated_data):
        new_cycle = validated_data.get('cycle')
        if new_cycle:
            if instance.cycle != new_cycle:
                # cycle change
                unpaid_invoices_count = Invoice.objects.filter(
                    items__service=instance, status=InvoiceStatus.ST_UNPAID).count()
                if unpaid_invoices_count > 0:
                    raise ValidationError(detail={
                        'cycle': _('You cannot change cycle for a service with unpaid invoices')
                    })
                for service_conf_opt in instance.configurable_options.all():
                    configurable_option = service_conf_opt.option
                    if not config_option_cycles_match_product(
                            configurable_option=configurable_option,
                            product=instance.product
                    ):
                        raise serializers.ValidationError(
                            _('Cannot change cycle, service configurable options cycles do not match service related '
                              'product cycles.')
                        )
                    conf_opt_cycle = configurable_option.cycles.filter(
                        currency=new_cycle.currency,
                        cycle=new_cycle.cycle,
                        cycle_multiplier=new_cycle.cycle_multiplier,
                    ).first()
                    if conf_opt_cycle:
                        service_conf_opt.unit_price = conf_opt_cycle.price
                        if not service_conf_opt.quantity:
                            service_conf_opt.price = service_conf_opt.unit_price
                        else:
                            service_conf_opt.price = service_conf_opt.quantity * service_conf_opt.unit_price
                        service_conf_opt.setup_fee = conf_opt_cycle.setup_fee
                        service_conf_opt.save()
                    else:
                        serializers.ValidationError(
                            _('Cannot change cycle because related configurable options could not be updated with '
                              'values from configurable options of new cycle')
                        )

        return super().update(instance=instance, validated_data=validated_data)
