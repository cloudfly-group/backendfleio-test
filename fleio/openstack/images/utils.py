from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


def is_valid_ascii(value):
    try:
        value.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


def validate_ascii_properties(value: str or dict):
    # TODO(tomo): show error for specific properties if possible.
    # right now, we show a generic error if one property does not contain ascii
    ascii_err_msg = _('Only ASCII characters are allowed for properties and values')
    if isinstance(value, str) and not is_valid_ascii(value):
        raise serializers.ValidationError(detail=ascii_err_msg)
    elif isinstance(value, dict):
        for key, val in value.items():
            if isinstance(key, str) and not is_valid_ascii(key):
                raise serializers.ValidationError(detail=ascii_err_msg)
            if isinstance(val, str) and not is_valid_ascii(val):
                raise serializers.ValidationError(detail=ascii_err_msg)
    return value
