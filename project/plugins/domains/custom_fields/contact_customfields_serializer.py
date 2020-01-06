from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.custom_fields.validation import validate_custom_field
from plugins.domains.custom_fields.contact_custom_field_definition import ContactCustomFieldDefinition
from plugins.domains.models import ContactCustomField


class ContactCustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCustomField
        fields = ('name', 'label', 'value')
        read_only_fields = ('label', )

    def __init__(self, *args, **kwargs):
        self.fields_definition = ContactCustomFieldDefinition()
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        field_name = data.get('name', None)
        field_label = data.get('label', None)
        field_definition = self.fields_definition.definition.get(field_name, None)
        if field_definition:
            validate_custom_field(field_definition, None, data['value'])

            # TODO: implement validation for all field types here
            if field_definition.get('type', 'string') == 'check':
                data['value'] = 'true' if data['value'] else 'false'
            if field_definition.get('required', False):
                if data['value'] is None:
                    raise ValidationError(
                        detail={
                            field_name: _('This field cannot be null')
                        }
                    )

        return {
            'name': field_name,
            'label': field_label,
            'value': data['value']
        }

    def validate(self, attrs):
        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        field_definition = self.fields_definition.definition.get(representation['name'], None)
        if field_definition and field_definition.get('type', 'string') == 'check':
            representation['value'] = True if representation['value'] == 'true' else False
        return representation
