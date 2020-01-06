from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from plugins.domains.utils.domain import DomainUtils


def tld_name_validator(tld_name: str):
    if not DomainUtils.validate_tld_name(tld_name=tld_name):
        raise serializers.ValidationError(_('Must contain a valid tld name, starting with "."'))


def domain_name_validator(domain_name: str):
    if not DomainUtils.validate_domain_name(domain_name=domain_name):
        raise serializers.ValidationError(_('Must contain a valid domain name, containing at least a "."'))
