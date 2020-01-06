import logging
import os

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.billing.models import ClientCredit
from fleio.billing.modules.factory import module_factory
from fleio.billing.utils import cdecimal
from fleio.core.clients.serializers import ClientCreditMinSerializer
from fleio.core.custom_fields.client_customfield_definition import ClientCustomFieldDefinition
from fleio.core.custom_fields.client_customfields_serializer import ClientCustomFieldSerializer
from fleio.core.drf import validate_vat_id
from fleio.core.models import Client
from fleio.core.models import ClientCustomField
from fleio.core.models import ClientGroup
from fleio.core.models import Configuration
from fleio.core.models import Currency
from fleio.core.models import UserToClient
from fleio.core.models import settings
from fleio.core.signals import client_created
from fleio.core.validation_utils import validate_client_limit
from fleio.osbilling.models import PricingPlan
from fleio.osbilling.models import ServiceDynamicUsage
from fleio.osbilling.models import ServiceDynamicUsageHistory
from fleio.osbilling.service_helper import ServiceHelper
from fleio.reseller.utils import client_reseller_resources
from fleio.reseller.utils import reseller_suspend_instead_of_terminate
from fleio.utils.files import save_uploaded_file
from fleiostaff.core.users.serializers import StaffUserSerializer

LOG = logging.getLogger(__name__)


class UserToClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToClient
        fields = '__all__'


class ChangeCreditSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0)
    currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        required=False,
        allow_empty=True,
        allow_null=True,
    )
    exchange_rate = serializers.DecimalField(max_digits=8, decimal_places=5, default=1)
    source_amount = serializers.DecimalField(max_digits=14, decimal_places=2, required=False)
    source_currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        required=False,
        allow_empty=True,
        allow_null=True,
    )
    add_credit = serializers.BooleanField()
    external_source = serializers.BooleanField(default=False)

    def validate(self, attrs):
        attrs = super().validate(attrs=attrs)
        client_credit = self.instance.get_remaining_credit(0, attrs['currency'])
        serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0).run_validation(
            attrs['amount'] + client_credit
        )
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ConfigurationIdSerializer(serializers.Serializer):
    configuration = serializers.CharField(max_length=36)


class StaffClientBriefSerializer(serializers.ModelSerializer):
    suspend_instead_of_terminate = serializers.SerializerMethodField(read_only=True)
    configuration_name = serializers.SerializerMethodField(read_only=True)
    group_name = serializers.SerializerMethodField(read_only=True)
    reseller_client_details = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_suspend_instead_of_terminate(client: Client):
        return client.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(
            client=client,
        )

    @staticmethod
    def get_configuration_name(client):
        return getattr(client, 'configuration_name', '')

    @staticmethod
    def get_group_name(client):
        group_name = getattr(client, 'group_name', '')
        return group_name if group_name is not None else ''

    @staticmethod
    def get_reseller_client_details(client: Client):
        if client.reseller_resources:
            return {
                'name': client.reseller_resources.service.client.name,
                'id': client.reseller_resources.service.client.id,
            }
        else:
            return None

    class Meta:
        model = Client
        fields = ('id', 'name', 'first_name', 'last_name', 'company', 'city', 'country', 'state', 'date_created',
                  'currency', 'phone', 'country_name', 'long_name', 'email', 'vat_id', 'status', 'uptodate_credit',
                  'suspend_instead_of_terminate', 'configuration_name', 'group_name', 'outofcredit_datetime',
                  'reseller_client_details')
        read_only_fields = ('id', 'name', 'country_name', 'long_name', 'currency', 'status', 'uptodate_credit',
                            'configuration_name', 'group_name', 'tax_exempt', 'outofcredit_datetime',
                            'reseller_client_details')


class ServiceDynamicUsageSerializer(serializers.ModelSerializer):
    """OpenStack Billing plan brief serializer"""

    class Meta:
        model = ServiceDynamicUsage
        fields = ('id', 'plan', 'start_date', 'end_date')


class StaffClientSerializer(serializers.ModelSerializer):
    suspend_instead_of_terminate = serializers.SerializerMethodField(read_only=True)
    credits = ClientCreditMinSerializer(many=True, read_only=True)
    custom_fields = serializers.SerializerMethodField()
    has_openstack_services = serializers.SerializerMethodField()
    openstack_billing_plans = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    reseller_client = serializers.SerializerMethodField()
    belongs_to_reseller = serializers.SerializerMethodField()
    reseller_client_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'name', 'first_name', 'last_name', 'company', 'city', 'country', 'state', 'date_created',
                  'currency', 'phone', 'country_name', 'long_name', 'fax', 'users', 'address1', 'address2', 'email',
                  'zip_code', 'vat_id', 'suspend_instead_of_terminate', 'credits', 'custom_fields', 'uptodate_credit',
                  'has_openstack_services', 'status', 'tax_exempt', 'outofcredit_datetime', 'openstack_billing_plans',
                  'group_name', 'reseller_client', 'belongs_to_reseller', 'reseller_client_details')
        read_only_fields = ('id', 'date_created', 'users', 'currency', 'credits', 'status', 'outofcredit_datetime',
                            'openstack_billing_plans', 'reseller_client_details')

    @staticmethod
    def get_suspend_instead_of_terminate(client: Client):
        return client.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(
            client=client,
        )

    @staticmethod
    def get_belongs_to_reseller(client: Client):
        return client.reseller_resources is not None

    @staticmethod
    def get_custom_fields(client):
        cf_qs = ClientCustomField.objects.filter(
            client=client,
            name__in=ClientCustomFieldDefinition().definition.keys()
        )
        return ClientCustomFieldSerializer(instance=cf_qs, many=True).data

    @staticmethod
    def get_is_reseller(client: Client):
        return True if client_reseller_resources(client=client) else False

    @staticmethod
    def get_group_name(client):
        group = client.groups.first()
        return group.name if group else _('n/a')

    @staticmethod
    def get_has_openstack_services(client):
        # TODO: do a proper implementation of this
        return client.first_project is not None

    @staticmethod
    def get_openstack_billing_plans(client):
        return [
            {
                'id': plan.id,
                'name': plan.name
            } for plan in PricingPlan.objects.for_reseller(client.reseller_resources)
        ]

    @staticmethod
    def get_reseller_client(client: Client):
        if client.reseller_resources:
            return client.reseller_resources.service.client.id
        else:
            return None

    @staticmethod
    def get_reseller_client_details(client: Client):
        if client.reseller_resources:
            return {
                'name': client.reseller_resources.service.client.name,
                'id': client.reseller_resources.service.client.id,
            }
        else:
            return None

    def validate(self, attrs):
        vat_id = attrs.get('vat_id')
        country_code = attrs.get('country', None)
        if vat_id and country_code:
            valid_vat, message = validate_vat_id(vat_id=vat_id, country_code=country_code)
            if not valid_vat:
                raise serializers.ValidationError({'vat_id': message})
        return super(StaffClientSerializer, self).validate(attrs)


class StaffCreateClientSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(slug_field='name',
                                          queryset=ClientGroup.objects.all(),
                                          many=True,
                                          required=False)
    configuration = serializers.SlugRelatedField(slug_field='name',
                                                 queryset=Configuration.objects.all(),
                                                 required=False)
    user = StaffUserSerializer(write_only=True, required=False)
    create_auto_order_service = serializers.BooleanField(required=False, default=False)
    auto_order_service_external_billing_id = serializers.CharField(
        max_length=38, allow_null=True, allow_blank=True, required=False
    )
    custom_fields = ClientCustomFieldSerializer(many=True, required=False)
    reseller_client = serializers.IntegerField(required=False, allow_null=True, default=0)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'company', 'address1',
                  'address2', 'city', 'country', 'state', 'zip_code',
                  'phone', 'fax', 'email', 'vat_id', 'groups', 'external_billing_id',
                  'currency', 'configuration', 'user', 'create_auto_order_service',
                  'auto_order_service_external_billing_id', 'custom_fields', 'reseller_client')
        read_only_fields = ('id',)

    def validate(self, attrs):
        cf = ClientCustomFieldDefinition()
        try:
            cfs = cf.validate(new_fields=attrs,
                              instance=self.instance)
        except Exception as e:
            raise serializers.ValidationError({'custom_fields': e})
        attrs['custom_fields'] = [{'name': k, 'value': v} for k, v in iter(cfs.items())]

        vat_id = attrs.get('vat_id')
        country_code = attrs.get('country', None)
        if vat_id and country_code:
            valid_vat, message = validate_vat_id(vat_id=vat_id, country_code=country_code)
            if not valid_vat:
                raise serializers.ValidationError({'vat_id': message})

        if not validate_client_limit():
            raise serializers.ValidationError({
                'non_field_errors': _('License client limit reached. Please check your license'),
            })

        return super(StaffCreateClientSerializer, self).validate(attrs)

    def create(self, validated_data):
        create_auto_order_service = validated_data.pop('create_auto_order_service', False)
        auto_order_service_external_billing_id = validated_data.pop('auto_order_service_external_billing_id', None)
        request_user = None
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            request_user = request.user
        user = validated_data.pop('user', None)
        groups = validated_data.pop('groups', list())
        custom_fields = validated_data.pop('custom_fields', None)
        reseller_client = validated_data.pop('reseller_client', None)  # type: Client
        if reseller_client:
            reseller_client_obj = Client.objects.get(id=reseller_client)
            validated_data['reseller_resources'] = client_reseller_resources(client=reseller_client_obj)
        with transaction.atomic():
            # NOTE(tomo): We do all database actions first and create the
            # project which also calls the nova API, afterwards.
            db_client = super(StaffCreateClientSerializer, self).create(validated_data)
            if user:
                db_user = get_user_model().objects.create_user(**user)
                # TODO(tomo): is_client_admin should be configurable
                UserToClient.objects.create(user=db_user, client=db_client, is_client_admin=True)
            if isinstance(groups, list):
                for group in groups:
                    db_client.groups.add(group)

            # Create the project if everything above is in order (calls the OpenStack API)
            if create_auto_order_service:
                client_created.send(sender=self.__class__, client=db_client, create_auto_order_service=True,
                                    auto_order_service_external_billing_id=auto_order_service_external_billing_id,
                                    request_user=request_user.id if request_user else None)

            for field in custom_fields:
                db_client.custom_fields.create(
                    name=field['name'],
                    value=field['value'],
                    value_type='string'
                )

        return db_client


class StaffClientUpdateSerializer(serializers.ModelSerializer):
    custom_fields = ClientCustomFieldSerializer(many=True)
    reseller_client = serializers.IntegerField(required=False, allow_null=True, default=0)

    class Meta:
        model = Client
        exclude = ('users', 'groups',)  # FIXME(tomo): Allow users, groups... update
        read_only_fields = ('id',)

    def validate(self, attrs):
        attrs = super(StaffClientUpdateSerializer, self).validate(attrs)
        cf = ClientCustomFieldDefinition()
        try:
            cfs = cf.validate(new_fields=attrs,
                              instance=self.instance)
        except Exception as e:
            raise serializers.ValidationError({'custom_fields': e})
        attrs['custom_fields'] = [{'name': k, 'value': v} for k, v in iter(cfs.items())]
        # Validate VAT ID
        vat_id = attrs.get('vat_id')
        country_code = attrs.get('country', None)
        if vat_id and country_code:
            valid_vat, message = validate_vat_id(vat_id=vat_id, country_code=country_code)
            if not valid_vat:
                raise serializers.ValidationError({'vat_id': message})
        return attrs

    def update(self, instance, validated_data):
        custom_fields = validated_data.pop('custom_fields')
        custom_fields_names = []
        for field in custom_fields:
            instance.custom_fields.update_or_create(name=field['name'],
                                                    defaults={'value': field['value'],
                                                              'value_type': 'string'})
            custom_fields_names.append(field['name'])
        instance.custom_fields.exclude(name__in=custom_fields_names).delete()
        reseller_client = validated_data.pop('reseller_client', None)  # type: Client
        if reseller_client:
            reseller_client_obj = Client.objects.get(id=reseller_client)
            validated_data['reseller_resources'] = client_reseller_resources(client=reseller_client_obj)
        else:
            validated_data['reseller_resources'] = None

        # if someone changes currency, make sure the client has new ClientCredit in that currency
        old_currency = instance.currency
        new_currency = validated_data.get('currency', None)
        if new_currency and isinstance(new_currency, Currency):
            if old_currency.code != new_currency.code:
                try:
                    # when changing client currency, also empty the cart so a new cart will get created with the new
                    # currency
                    cart = instance.fleio_cart
                    cart.delete()
                except Client.fleio_cart.RelatedObjectDoesNotExist:
                    pass
                credit_exists = ClientCredit.objects.filter(client=instance, currency=new_currency).count()
                if credit_exists == 0:
                    try:
                        ClientCredit.objects.create(client=instance, currency=new_currency)
                    except IntegrityError:
                        pass

        instance = super(StaffClientUpdateSerializer, self).update(instance, validated_data)  # type: Client
        if instance.first_project:
            service = instance.first_project.service
            if instance.reseller_resources:
                ServiceHelper.set_new_reseller(service)
            else:
                ServiceHelper.clear_reseller(service)

        return instance


class UserIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


class ObjectLoadRangeSerializer(serializers.Serializer):
    # name = serializers.CharField()
    lower_limit = serializers.IntegerField(required=False)
    upper_limit = serializers.IntegerField(required=False)


class ClientUnsettledHistorySerializer(serializers.ModelSerializer):
    """
    This is here only for external billing eg: WHMCS.
    Remove this once we find another way in order to avoid an OpenStack billing
    dependency here.
    """

    class Meta:
        model = ServiceDynamicUsageHistory
        fields = ('id', 'start_date', 'end_date', 'state')


class OverdueClientSerializer(serializers.ModelSerializer):
    """This only works when annotate_main_credit is used on a queryset"""
    effective_credit_limit = serializers.SerializerMethodField()
    unsettled_periods = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'external_billing_id', 'currency', 'uptodate_credit',
                  'effective_credit_limit', 'has_billing_agreement', 'unsettled_periods')

    @staticmethod
    def get_effective_credit_limit(obj):
        if obj.has_billing_agreement:
            return cdecimal(obj.billing_settings.credit_limit_with_agreement, q='.01')
        else:
            return cdecimal(obj.billing_settings.credit_limit, q='.01')

    @staticmethod
    def get_unsettled_periods(client: Client):
        services_unsettled_periods = []
        for service in client.services.all():
            billing_module = module_factory.get_module_instance(service=service)
            service_unsettled_periods = billing_module.get_service_unsettled_periods(service=service)
            services_unsettled_periods = services_unsettled_periods + service_unsettled_periods
        return ClientUnsettledHistorySerializer(services_unsettled_periods, many=True).data


class BillingAgreementsSetSerializer(serializers.Serializer):
    """Used by external billing systems to update the
     billing agreement field on a client"""
    uuid = serializers.CharField(max_length=64)
    agreement = serializers.BooleanField()
    client = serializers.HiddenField(default=None)

    class Meta:
        fields = '__all__'

    def validate(self, attrs):
        attrs = super(BillingAgreementsSetSerializer, self).validate(attrs)
        try:
            attrs['client'] = Client.objects.get(external_billing_id=attrs['uuid'])
        except (Client.DoesNotExist, Client.MultipleObjectsReturned):
            LOG.error('Client with external billing ID {} not found for changing billing agreement status'.format(
                attrs.get('uuid')
            ))
        return attrs

    def update(self, instance, validated_data):
        client = validated_data.get('client')
        if client:
            client.has_billing_agreement = validated_data['agreement']
            client.save(update_fields=['has_billing_agreement'])
            return client
        return None

    def create(self, validated_data):
        return self.update(instance=validated_data.get('client'), validated_data=validated_data)


class MassEmailSerializer(serializers.Serializer):
    from_name_addr = serializers.CharField(
        max_length=2048, required=True, allow_blank=False, allow_null=False
    )
    subject = serializers.CharField(
        max_length=2018, required=True, allow_blank=True, allow_null=True,
    )
    body = serializers.CharField(
        max_length=10240, required=True, allow_blank=True, allow_null=True,
    )
    send_batch_size = serializers.IntegerField(required=True, allow_null=False)
    send_interval = serializers.IntegerField(required=True, allow_null=False)
    filter = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=4096)
    search = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    attachments = serializers.DictField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        attachments = {}
        attachments_ok = True
        for file_data_key in data:  # type: str
            if file_data_key.startswith('file_data_'):
                file_name_key = file_data_key.replace('file_data_', 'file_name_')
                file_data = data[file_data_key]
                if file_data.size > settings.MAX_EMAIL_ATTACHMENT_SIZE:
                    attachments_ok = False
                    break
                saved_file_name = save_uploaded_file(file_data)
                attachments[data[file_name_key]] = (saved_file_name, file_data.content_type)
        if not attachments_ok:
            for attachment_name, attachment_file_path in attachments.items():
                try:
                    os.delete(attachment_file_path)
                except Exception as e:
                    del e  # unused
            raise ValidationError('Attachment is to big')
        validated_data['attachments'] = attachments
        return validated_data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
