import logging
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .conf import conf
from . import utils

LOG = logging.getLogger(__name__)


class RomcardCallbackSerializer(serializers.Serializer):
    TERMINAL = serializers.CharField(max_length=255, required=False)
    TRTYPE = serializers.IntegerField()
    ACTION = serializers.IntegerField()
    RRN = serializers.CharField(max_length=255, allow_blank=True)
    ORDER = serializers.CharField(max_length=255)
    RC = serializers.CharField(max_length=3)
    AMOUNT = serializers.DecimalField(max_digits=14, decimal_places=2)
    INT_REF = serializers.CharField(max_length=255, allow_blank=True)
    APPROVAL = serializers.CharField(max_length=32, required=False)
    CURRENCY = serializers.CharField(max_length=3)
    DESC = serializers.CharField(max_length=255, required=False)
    P_SIGN = serializers.CharField(max_length=255)
    NONCE = serializers.CharField(max_length=255)
    TIMESTAMP = serializers.CharField(max_length=32)
    MESSAGE = serializers.CharField(max_length=255, allow_blank=True)

    def validated_ORDER(self, value):
        return utils.invoice_id_from_api(value)

    def validate_TERMINAL(self, value):
        if value != conf.terminal:
            raise ValidationError(detail='Terminal mismatch')
        return value

    def validate_ACTION(self, value):
        if value not in utils.RomcardAction.LIST_ACTIONS:
            raise ValidationError(detail='Invalid or unknown ACTION value')
        return value

    def validate(self, attrs):
        """Validate P_SIGN"""
        trtype = attrs.get('TRTYPE', None)
        if trtype == 0:
            p_sign_args = (conf.encryption_key,
                           conf.terminal,
                           attrs.get('TRTYPE', ''),
                           attrs.get('ORDER', ''),
                           attrs.get('AMOUNT', ''),
                           attrs.get('CURRENCY', ''),
                           attrs.get('DESC', ''),
                           attrs.get('ACTION', ''),
                           attrs.get('RC', ''),
                           attrs.get('MESSAGE', ''),
                           attrs.get('RRN', ''),
                           attrs.get('INT_REF', ''),
                           attrs.get('APPROVAL', ''),
                           attrs.get('TIMESTAMP', ''),
                           attrs.get('NONCE', ''))
        elif trtype in (21, 24, 27):
            p_sign_args = (conf.encryption_key,
                           attrs.get('ACTION', ''),
                           attrs.get('RC', ''),
                           attrs.get('MESSAGE', ''),
                           attrs.get('TRTYPE', ''),
                           attrs.get('AMOUNT', ''),
                           attrs.get('CURRENCY', ''),
                           attrs.get('ORDER', ''),
                           attrs.get('RRN', ''),
                           attrs.get('INT_REF', ''),
                           attrs.get('TIMESTAMP', ''),
                           attrs.get('NONCE', ''))
        elif trtype == 171:
            p_sign_args = (conf.encryption_key,
                           conf.terminal,
                           attrs.get('TRTYPE', ''),
                           attrs.get('AMOUNT', ''),
                           attrs.get('CURRENCY', ''),
                           attrs.get('ORDER', ''),
                           attrs.get('RRN', ''),
                           attrs.get('INT_REF', ''),
                           attrs.get('APPROVAL', ''),
                           attrs.get('TIMESTAMP', ''),
                           attrs.get('NONCE', ''))
        else:
            LOG.error('Unknown TRTYPE ({})'.format(trtype))
            raise ValidationError(detail='Unknown TRTYPE')
        p_sign = utils.calculate_p_sign(*p_sign_args)
        if p_sign != attrs['P_SIGN']:
            LOG.error('Invalid gateway callback (Error: P_SIGN mismatch)')
            raise ValidationError(detail='Invalid request')
        return attrs
