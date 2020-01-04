from django.utils.module_loading import import_string


def validate_custom_field(field_definition, instance: object = None, value: str = None):
    if field_definition['validator']:
        try:
            validator = import_string(field_definition['validator'])
        except ImportError:
            pass
        else:
            validator(instance, value)
