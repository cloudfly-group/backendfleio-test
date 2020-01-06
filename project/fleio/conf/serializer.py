from __future__ import unicode_literals

from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.utils.field_mapping import ClassLookupDict
from fleio.conf import options
from fleio.conf.base import ConfigOpts


ALL_FIELDS = '__all__'


class URIField(serializers.CharField):
    """Serializer URI field supporting various schemes"""
    default_error_messages = {
        'invalid': _('Enter a valid URL, using the following schemes: {}')
    }

    def __init__(self, **kwargs):
        schemes = kwargs.pop('schemes', ['http', 'https', 'ftp', 'ftps'])
        super(URIField, self).__init__(**kwargs)
        validator = URLValidator(schemes=schemes, message=self.error_messages['invalid'].format(
            ', '.join(scheme for scheme in schemes)
        ))
        self.validators.append(validator)


class ConfSerializer(serializers.Serializer):
    serializer_field_mapping = {
        options.IntegerOpt: serializers.IntegerField,
        options.StringOpt: serializers.CharField,
        options.DjangoStringTemplateOpt: serializers.CharField,
        options.DecimalOpt: serializers.DecimalField,
        options.URIOpt: URIField,
        options.BoolOpt: serializers.BooleanField,
        options.JsonOpt: serializers.JSONField,
        options.ListOpt: serializers.ListField,
        options.DictOpt: serializers.DictField
    }
    serializer_choice_field = serializers.ChoiceField

    class Meta:
        extra_kwargs = {}
        fields = ALL_FIELDS

    def __init__(self, instance=None, *args, **kwargs):
        self.meta_conf_class = getattr(self.Meta, 'conf_class', None)
        if self.meta_conf_class is None:  # NOTE(tomo): Instance of ConfigOpts required if Meta class not set
            assert isinstance(instance, ConfigOpts), 'ConfSerializer requires a ConfigOpts instance when initialized'
        elif instance is None:  # NOTE(tomo): Initialize the Instance with the Meta conf class
            instance = self.meta_conf_class()
        self.meta_exclude = getattr(self.Meta, 'exclude', None)
        self.meta_fields = getattr(self.Meta, 'fields', ALL_FIELDS)
        if self.meta_exclude:
            self.meta_fields = None
        super(ConfSerializer, self).__init__(instance=instance, *args, **kwargs)

    def get_declared_fields(self):
        """Get and check manually declared fields on the serializer class"""
        declared_fields = super(ConfSerializer, self).get_fields()
        # Check declared fields are present in meta_fields and are not listed in meta_exclude
        for f_name in declared_fields:
            if self.meta_fields and self.meta_fields != ALL_FIELDS and f_name not in self.meta_fields:
                raise TypeError('{} {} field declared but not included in the Meta.fields list'
                                .format(self.__class__.__name__, f_name))
            if self.meta_exclude and f_name in self.meta_exclude:
                raise TypeError('{} {} field declared but added to Meta.exclude list'
                                .format(self.__class__.__name__, f_name))
        return declared_fields

    @staticmethod
    def get_field_kwargs(option_instance, extra_kwargs):
        # Default value:
        if option_instance.default is not options.Empty and 'default' not in extra_kwargs:
            extra_kwargs['default'] = option_instance.default
        # allow_null
        if option_instance.allow_null:
            if 'allow_null' not in extra_kwargs:
                extra_kwargs['allow_null'] = True
                if isinstance(option_instance, options.StringOpt):  # Allow blank for string only (choices also works)
                    extra_kwargs['allow_blank'] = True
        # encrypted should be write_only and not required
        if option_instance.encrypted:
            if 'write_only' not in extra_kwargs:
                extra_kwargs['write_only'] = True
            if 'required' not in extra_kwargs:
                extra_kwargs['required'] = False
        # max_length
        if hasattr(option_instance.type, 'max_length') and 'max_length' not in extra_kwargs:
            if option_instance.type.max_length:
                extra_kwargs['max_length'] = option_instance.type.max_length
        # URI schemes
        if hasattr(option_instance, 'schemes') and option_instance.schemes and 'schemes' not in extra_kwargs:
            extra_kwargs['schemes'] = option_instance.schemes  # URL Field with scheme validation
        # Min Max values
        if hasattr(option_instance.type, 'min') and 'min_value' not in extra_kwargs:
            extra_kwargs['min_value'] = option_instance.type.min
        if hasattr(option_instance.type, 'max') and 'max_value' not in extra_kwargs:
            extra_kwargs['max_value'] = option_instance.type.max
        # Max digits, decimal places and coerce to string for decimalOpt
        if isinstance(option_instance, options.DecimalOpt):
            extra_kwargs['max_digits'] = option_instance.type.max_digits
            extra_kwargs['decimal_places'] = option_instance.type.decimal_places
            extra_kwargs['coerce_to_string'] = option_instance.type.coerce_to_string
        # help_text and label
        for other_kwarg in ('help_text', 'label'):
            other_kwarg_value = getattr(option_instance, other_kwarg, None)
            if other_kwarg not in extra_kwargs and other_kwarg_value:
                extra_kwargs[other_kwarg] = other_kwarg_value
        return extra_kwargs

    def get_fields(self):
        """Build and return a list with all the serializer fields"""
        fields = OrderedDict()
        declared_fields = self.get_declared_fields()
        field_classes = ClassLookupDict(self.serializer_field_mapping)
        fields_extra_kwargs = getattr(self.Meta, 'extra_kwargs', {})

        for opt_name, opt_class in iter(self.instance.declared_options.items()):
            # Add or exclude any fields declared in Meta.fields or .exclude
            if self.meta_fields and self.meta_fields != ALL_FIELDS and opt_name not in self.meta_fields:
                continue
            if self.meta_exclude and opt_name in self.meta_exclude:
                continue
            # If the field is already declared on the serializer, use it
            if opt_name in declared_fields:
                fields[opt_name] = declared_fields[opt_name]
                continue
            # Create other new fields based on conf option definition
            extra_kwargs = fields_extra_kwargs.get(opt_name, {})
            if getattr(opt_class, 'choices', None) is not None:
                # Every field with choices defined, will be represented as a ChoiceField
                fields[opt_name] = serializers.ChoiceField(choices=opt_class.choices, **extra_kwargs)
            else:
                self.get_field_kwargs(option_instance=opt_class, extra_kwargs=extra_kwargs)
                # List or Dict field with child
                if isinstance(opt_class, (options.ListOpt, options.DictOpt, )) and 'child' not in extra_kwargs:
                    child_kwargs = {}
                    if getattr(opt_class.item_type, 'choices', None) is not None:
                        child = serializers.ChoiceField(choices=opt_class.item_type.choices)
                    else:
                        child = field_classes[opt_class.item_type]
                        self.get_field_kwargs(option_instance=opt_class.item_type, extra_kwargs=child_kwargs)
                    extra_kwargs['child'] = child(**child_kwargs)

                fields[opt_name] = field_classes[opt_class](**extra_kwargs)

        for field_name, field_instance in iter(declared_fields.items()):
            # NOTE(tomo): Add any serializer declared fields that are not part of the config class
            if field_name not in fields and (self.meta_fields == ALL_FIELDS or field_name in self.meta_fields):
                fields[field_name] = field_instance
        return fields

    def update(self, instance, validated_data):
        for field, value in iter(validated_data.items()):
            try:
                setattr(self.instance, field, value)
            except ValueError as e:
                raise serializers.ValidationError(detail={field: ['{}'.format(e)]})
        self.instance.save()
        return self.instance

    def create(self, validated_data):
        raise serializers.ValidationError('Settings can only be updated')
