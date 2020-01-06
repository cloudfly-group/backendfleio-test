from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from plugins.domains.models import Domain
from plugins.domains.models.domain import DomainStatus

from .nameserver import NameserverSerializer
from .tld import TLDSerializer


class DomainSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    tld = TLDSerializer(read_only=True, required=False)
    nameservers = NameserverSerializer(many=True, read_only=True)
    dns_management = serializers.SerializerMethodField()
    email_forwarding = serializers.SerializerMethodField()
    id_protection = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = '__all__'

    @staticmethod
    def get_dns_management(domain):
        if not domain.service:
            return False

        return domain.service.configurable_options.filter(option=domain.tld.dns_option).exists()

    @staticmethod
    def get_email_forwarding(domain):
        if not domain.service:
            return False

        return domain.service.configurable_options.filter(option=domain.tld.email_option).exists()

    @staticmethod
    def get_id_protection(domain):
        if not domain.service:
            return False

        return domain.service.configurable_options.filter(option=domain.tld.id_option).exists()

    @staticmethod
    def get_status_display(instance):
        return DomainStatus.domain_status_map.get(instance.status, _('n/a'))
