from fleio.conf import options
from fleio.conf.base import ConfigOpts
from fleio.conf.models import Configuration
from fleio.conf.serializer import ConfSerializer
from fleio.core.models import Client


class OpenstackSettings(ConfigOpts):
    auto_cleanup_images = options.BoolOpt(default=False)
    auto_cleanup_number_of_days = options.IntegerOpt(default=14)
    auto_cleanup_image_types = options.ListOpt(
        default=['ami', 'ari', 'aki', 'vhd', 'vmdk', 'raw', 'qcow2', 'vdi', 'iso'],
        item_type=options.StringOpt(),
    )

    class Meta:
        section = 'OPENSTACK'

    @staticmethod
    def for_client(client: Client) -> 'OpenstackSettings':
        if not client:
            return OpenstackSettings()

        if client.configuration:
            return OpenstackSettings(configuration_id=client.configuration.id)
        else:
            try:
                default_config = Configuration.objects.default(reseller_resources=client.reseller_resources)
            except Configuration.DoesNotExist:
                return OpenstackSettings()
            else:
                return OpenstackSettings(configuration_id=default_config.id)


class OpenstackSettingsSerializer(ConfSerializer):
    class Meta:
        conf_class = OpenstackSettings
        fields = (
            'auto_cleanup_images',
            'auto_cleanup_number_of_days',
            'auto_cleanup_image_types',
        )
