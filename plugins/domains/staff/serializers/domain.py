from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.billing.utils import cdecimal
from plugins.domains.models import Domain
from plugins.domains.models.domain import DomainStatus
from plugins.domains.staff.serializers import ContactSerializer

from .nameserver import NameserverSerializer
from .tld import TLDSerializer


class DomainSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    status_display = serializers.SerializerMethodField()
    tld = TLDSerializer(read_only=True, required=False)
    price_display = serializers.SerializerMethodField()
    nameservers = NameserverSerializer(many=True, read_only=True)
    last_registrar_name = serializers.SerializerMethodField()
    dns_management = serializers.SerializerMethodField()
    email_forwarding = serializers.SerializerMethodField()
    id_protection = serializers.SerializerMethodField()
    contact = ContactSerializer(read_only=True)
    client_id = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = '__all__'

    @staticmethod
    def get_client_id(domain):
        return domain.service.client.id if domain.service else domain.assigned_to_service.client.id

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

    @staticmethod
    def get_price_display(instance):
        if instance.service:
            return '{} {}'.format(
                cdecimal(instance.service.get_fixed_price()),
                instance.service.cycle.currency.code,
            )
        else:
            return None

    @staticmethod
    def get_last_registrar_name(domain):
        return domain.last_registrar.name if domain.last_registrar else _('n/a')
