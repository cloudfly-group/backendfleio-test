from django.db import IntegrityError
from rest_framework import serializers

from fleio.billing.models import ClientCredit
from fleio.core.custom_fields.client_customfield_definition import ClientCustomFieldDefinition
from fleio.core.custom_fields.client_customfields_serializer import ClientCustomFieldSerializer
from fleio.core.drf import validate_vat_id
from fleio.core.models import Client
from fleio.core.models import Currency


class ResellerClientUpdateSerializer(serializers.ModelSerializer):
    custom_fields = ClientCustomFieldSerializer(many=True)

    class Meta:
        model = Client
        exclude = ('users', 'groups',)  # FIXME(tomo): Allow users, groups... update
        read_only_fields = ('id',)

    def validate(self, attrs):
        attrs = super().validate(attrs)
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

        instance = super().update(instance, validated_data)  # type: Client

        return instance
