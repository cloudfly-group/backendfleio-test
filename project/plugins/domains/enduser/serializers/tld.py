from rest_framework import serializers

from plugins.domains.models import TLD
from plugins.domains.utils.drf.validators import tld_name_validator
from plugins.domains.utils.whois_config import whois_config


class TLDSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=65, validators=[tld_name_validator])
    whois_server_configured = serializers.SerializerMethodField(required=False)

    class Meta:
        model = TLD
        fields = '__all__'

    @staticmethod
    def get_whois_server_configured(instance):
        tld_name = instance.name.lower()
        if tld_name in whois_config.tld_whois_configurations:
            return True
        else:
            return False
