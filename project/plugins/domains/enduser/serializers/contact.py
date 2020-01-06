from django.db import transaction
from rest_framework import serializers

from fleio.core.drf import validate_vat_id
from plugins.domains.custom_fields.contact_custom_field_definition import ContactCustomFieldDefinition

from plugins.domains.custom_fields.contact_customfields_serializer import ContactCustomFieldSerializer
from plugins.domains.models import Contact


class CurrentClientDefault:
    """Serializer validator for default field"""

    def __init__(self, *args, **kwargs):
        del args, kwargs  # unused
        self.client = None

    def set_context(self, serializer_field):
        request = serializer_field.context.get('request')
        if request:
            current_client = request.user.clients.first()
            if current_client is not None:
                self.client = current_client

    def __call__(self):
        return self.client


class ContactSerializer(serializers.ModelSerializer):
    custom_fields = ContactCustomFieldSerializer(many=True)
    name = serializers.CharField(read_only=True)
    details = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = '__all__'

    @staticmethod
    def get_details(contact):
        contact_details = '{}({})\n{}, {}\n{}, {}'.format(
            contact.name,
            contact.email,
            contact.address1,
            contact.city,
            contact.state,
            contact.country
        )

        return contact_details

    def validate(self, attrs):
        vat_id = attrs.get('vat_id')
        country_code = attrs.get('country', None)
        if vat_id and country_code:
            valid_vat, message = validate_vat_id(vat_id=vat_id, country_code=country_code)
            if not valid_vat:
                raise serializers.ValidationError({'vat_id': message})
        return super().validate(attrs)


class ContactCreateSerializer(serializers.ModelSerializer):
    custom_fields = ContactCustomFieldSerializer(many=True, required=False)
    client = serializers.HiddenField(default=CurrentClientDefault())

    class Meta:
        model = Contact
        fields = '__all__'

    def validate(self, attrs):
        attrs = super().validate(attrs)
        cf = ContactCustomFieldDefinition()
        try:
            cfs = cf.validate(
                new_fields=attrs,
                instance=self.instance,
            )
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

    def create(self, validated_data):
        custom_fields = validated_data.pop('custom_fields', None)
        with transaction.atomic():
            new_contact = super().create(validated_data)
            for field in custom_fields:
                new_contact.custom_fields.create(
                    name=field['name'],
                    value=field['value'],
                    value_type='string',
                )
        return new_contact


class ContactUpdateSerializer(serializers.ModelSerializer):
    custom_fields = ContactCustomFieldSerializer(many=True)
    client = serializers.HiddenField(default=CurrentClientDefault())

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('id',)

    def validate(self, attrs):
        attrs = super(ContactUpdateSerializer, self).validate(attrs)
        cf = ContactCustomFieldDefinition()
        try:
            cfs = cf.validate(
                new_fields=attrs,
                instance=self.instance,
            )
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
        return super().update(instance, validated_data)
