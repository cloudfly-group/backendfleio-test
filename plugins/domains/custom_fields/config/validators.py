from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError


def validate_cnp(instance, value: str):
    del instance  # unused
    if not value:
        return

    if not value.isnumeric():
        raise ValidationError(
            detail={
                'rocnp': _('CNP should contain only digits.')
            }
        )
    if len(value) != 13:
        raise ValidationError(
            detail={
                'rocnp': _('CNP should be exactly 13 characters.')
            }
        )
