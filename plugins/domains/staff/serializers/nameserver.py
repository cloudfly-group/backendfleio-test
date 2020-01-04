from rest_framework import serializers

from plugins.domains.models.nameserver import Nameserver


class NameserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nameserver
        fields = '__all__'
