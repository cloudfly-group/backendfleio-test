from fleio.conf import options
from fleio.conf.base import ConfigOpts
from fleio.conf.models import Configuration
from fleio.conf.serializer import ConfSerializer
from fleio.core.models import Client


class DomainsSettings(ConfigOpts):
    allow_domain_registration = options.BoolOpt(default=True)
    allow_domain_transfer = options.BoolOpt(default=True)
    enable_default_tld = options.BoolOpt(default=False)
    default_tld = options.StringOpt(allow_null=True)
    enable_default_nameservers = options.BoolOpt(default=False)
    default_nameserver1 = options.StringOpt(allow_null=True)
    default_nameserver2 = options.StringOpt(allow_null=True)
    default_nameserver3 = options.StringOpt(allow_null=True)
    default_nameserver4 = options.StringOpt(allow_null=True)

    class Meta:
        section = 'DOMAINS'

    @staticmethod
    def for_client(client: Client) -> 'DomainsSettings':
        if not client:
            return DomainsSettings()

        if client.configuration:
            return DomainsSettings(configuration_id=client.configuration.id)
        else:
            try:
                default_config = Configuration.objects.default(reseller_resources=client.reseller_resources)
            except Configuration.DoesNotExist:
                return DomainsSettings()
            else:
                return DomainsSettings(configuration_id=default_config.id)


class DomainsSettingsSerializer(ConfSerializer):
    class Meta:
        conf_class = DomainsSettings
        fields = '__all__'
