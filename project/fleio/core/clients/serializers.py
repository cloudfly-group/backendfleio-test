from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.billing.serializers import ClientCreditMinSerializer
from fleio.core.custom_fields.client_customfield_definition import ClientCustomFieldDefinition
from fleio.core.custom_fields.client_customfields_serializer import ClientCustomFieldSerializer
from fleio.core.drf import validate_vat_id
from fleio.core.models import Client, ClientCustomField
from fleio.core.models import ClientGroup
from fleio.core.validation_utils import validate_client_limit


class ClientMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ClientWithExternalBillingMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'external_billing_id',)
        read_only_fields = ('id', 'external_billing_id',)


class ClientBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'first_name', 'last_name', 'company', 'city', 'country', 'state', 'date_created',
                  'currency', 'phone', 'country_name', 'long_name', 'email', 'vat_id', 'status', 'address1', 'zip_code')
        read_only_fields = ('id', 'name', 'country_name', 'long_name', 'currency', 'status')


class ClientSerializer(ClientBriefSerializer):
    """Client serializer, used to display the user clients details"""
    credits = ClientCreditMinSerializer(many=True, read_only=True)
    custom_fields = serializers.SerializerMethodField()
    has_openstack_services = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'name', 'first_name', 'last_name', 'company', 'city', 'country', 'state', 'date_created',
                  'currency', 'phone', 'country_name', 'long_name', 'fax', 'users', 'address1', 'address2', 'email',
                  'zip_code', 'vat_id', 'credits', 'custom_fields', 'has_openstack_services', 'status')
        read_only_fields = ('id', 'date_created', 'users', 'currency', 'credits', 'status')

    @staticmethod
    def get_has_openstack_services(client):
        # TODO - #1019: do a proper implementation of this
        return client.first_project is not None

    @staticmethod
    def get_custom_fields(client):
        cf_qs = ClientCustomField.objects.filter(
            client=client,
            name__in=ClientCustomFieldDefinition().definition.keys()
        )
        return ClientCustomFieldSerializer(instance=cf_qs, many=True).data

    def validate(self, attrs):
        vat_id = attrs.get('vat_id')
        country_code = attrs.get('country', None)
        if vat_id and country_code:
            valid_vat, message = validate_vat_id(vat_id=vat_id, country_code=country_code)
            if not valid_vat:
                raise serializers.ValidationError({'vat_id': message})
        return super(ClientSerializer, self).validate(attrs)


class CreateClientSerializer(serializers.ModelSerializer):
    custom_fields = ClientCustomFieldSerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'company', 'address1',
                  'address2', 'city', 'country', 'state', 'zip_code',
                  'phone', 'fax', 'email', 'vat_id', 'custom_fields')

    def validate(self, attrs):
        attrs = super(CreateClientSerializer, self).validate(attrs)
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

        if not validate_client_limit():
            raise serializers.ValidationError(
                {
                    'non_field_errors': _('Unable to create client, please contact support.')
                }
            )
        return attrs

    def create(self, validated_data):
        custom_fields = validated_data.pop('custom_fields', None)
        with transaction.atomic():
            new_client = super(CreateClientSerializer, self).create(validated_data)
            for field in custom_fields:
                new_client.custom_fields.create(name=field['name'],
                                                value=field['value'],
                                                value_type='string')
        if new_client.groups.count() == 0:
            default_group = ClientGroup.objects.filter(is_default=True).first()
            if default_group:
                new_client.groups.add(default_group)

        return new_client


class ClientUpdateSerializer(serializers.ModelSerializer):
    custom_fields = ClientCustomFieldSerializer(many=True)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'company', 'city', 'country', 'state',
                  'phone', 'country_name', 'fax', 'address1', 'address2',
                  'email', 'zip_code', 'vat_id', 'custom_fields',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        attrs = super(ClientUpdateSerializer, self).validate(attrs)
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
        return super(ClientUpdateSerializer, self).update(instance, validated_data)
