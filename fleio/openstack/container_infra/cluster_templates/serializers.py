import re
import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.openstack import models

LOG = logging.getLogger(__name__)

LABELS_REGEX = '([^=,]+)=([^\0]+?)(?=,[^,]+=|$)'


class ClusterTemplateSyncSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)

    class Meta:
        model = models.ClusterTemplate
        fields = '__all__'


class ClusterTemplateListSerializer(serializers.ModelSerializer):
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)

    class Meta:
        model = models.ClusterTemplate
        fields = ('client', 'name', 'id', 'created_at', 'image_id', 'coe',)


class ClusterTemplateSerializer(serializers.ModelSerializer):
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)

    class Meta:
        model = models.ClusterTemplate
        exclude = ('sync_version',)


class ClusterTemplateBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClusterTemplate
        fields = ('id', 'name', )
        read_only_fields = ('id', 'name', )


class ClusterTemplateCreateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    region = serializers.CharField()
    http_proxy = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    no_proxy = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    https_proxy = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    server_type = serializers.CharField()
    name = serializers.CharField()
    coe = serializers.CharField()
    image_id = serializers.CharField()
    public = serializers.BooleanField(default=False)
    registry_enabled = serializers.BooleanField(default=False)
    tls_disabled = serializers.BooleanField(default=False)
    keypair_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    flavor_id = serializers.CharField()
    master_flavor_id = serializers.CharField()
    volume_driver = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    docker_storage_driver = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    docker_volume_size = serializers.IntegerField(allow_null=True, default=None)
    insecure_registry = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    network_driver = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    external_network_id = serializers.CharField()
    fixed_network = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    fixed_subnet = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    dns_nameserver = serializers.CharField(default='8.8.8.8')
    master_lb_enabled = serializers.BooleanField(default=False)
    floating_ip_enabled = serializers.BooleanField(default=False)
    labels = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    def to_internal_value(self, data):
        data = super().to_internal_value(data=data)
        labels = data.get('labels')
        labels_formatted = []
        if labels:
            labels_formatted = re.findall(LABELS_REGEX, labels)
        if len(labels_formatted):
            as_dict = {item[0]: item[1] for item in labels_formatted}
            data['labels'] = as_dict
        return data

    @staticmethod
    def validate_labels(labels):
        if labels:
            match = re.match(LABELS_REGEX, labels)
            if not match:
                raise serializers.ValidationError(_('Invalid input for labels.'))
        return labels
