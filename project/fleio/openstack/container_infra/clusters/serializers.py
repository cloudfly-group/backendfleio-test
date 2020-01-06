import re
import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.openstack import models
from fleio.openstack.models.cluster import ClusterStatus
from fleio.openstack.container_infra.cluster_templates.serializers import ClusterTemplateBriefSerializer

LOG = logging.getLogger(__name__)

LABELS_REGEX = '([^=,]+)=([^\0]+?)(?=,[^,]+=|$)'


class ClusterSyncSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)
    status = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = models.Cluster
        fields = '__all__'

    def to_internal_value(self, data):
        data = super().to_internal_value(data=data)
        status_reason = data.get('status_reason')
        if status_reason:
            if len(status_reason) > 1024:
                data['status_reason'] = _('Status reason not available. Check in OpenStack.')
        return data


class ClusterUpdatedSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)

    class Meta:
        model = models.Cluster
        fields = ('sync_version', 'status', 'id', 'region',)


class ClusterListSerializer(serializers.ModelSerializer):
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)
    display_status = serializers.SerializerMethodField(read_only=True)
    under_task = serializers.SerializerMethodField(read_only=True)
    cluster_template = ClusterTemplateBriefSerializer(read_only=True)

    class Meta:
        model = models.Cluster
        fields = ('client', 'id', 'name', 'status', 'health_status', 'display_status', 'under_task',
                  'cluster_template', )

    @staticmethod
    def get_display_status(model):
        return ClusterStatus.choices.get(model.status)

    @staticmethod
    def get_under_task(model):
        if model.status in ClusterStatus.under_progress_statuses:
            return True
        return False


class ClusterResizeSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    node_count = serializers.IntegerField(default=1)
    nodes_to_remove = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    @staticmethod
    def validate_nodes_to_remove(nodes_to_remove):
        if nodes_to_remove:
            try:
                nodes_to_remove.split(',')
            except Exception as e:
                raise serializers.ValidationError(
                    _('Invalid list. Separate each node uuid using a comma. {}').format(str(e))
                )
        return nodes_to_remove

    def to_internal_value(self, data):
        value = super().to_internal_value(data=data)
        nodes_to_remove = value.get('nodes_to_remove', '')
        if nodes_to_remove is None or nodes_to_remove == '':
            value['nodes_to_remove'] = list()
        else:
            if nodes_to_remove == '':
                value['nodes_to_remove'] = None
            else:
                stripped_values = list()
                nodes_to_remove_as_list = nodes_to_remove.split(',')
                for node_to_remove in nodes_to_remove_as_list:
                    stripped_values.append(node_to_remove.strip())
                value['nodes_to_remove'] = stripped_values
        return value


class ClusterCreateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    name = serializers.CharField()
    keypair = serializers.CharField()
    flavor_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    master_flavor_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    docker_volume_size = serializers.IntegerField()
    create_timeout = serializers.IntegerField(default=0)
    master_count = serializers.IntegerField(default=1)
    node_count = serializers.IntegerField(default=1)
    cluster_template_id = serializers.CharField()
    discovery_url = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    labels = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    def to_internal_value(self, data):
        data = super().to_internal_value(data=data)
        labels = data.get('labels')
        if labels == '':
            data['labels'] = {}
        else:
            labels_formatted = []
            if labels:
                labels_formatted = re.findall(LABELS_REGEX, labels)
            if len(labels_formatted):
                as_dict = {item[0]: item[1] for item in labels_formatted}
                data['labels'] = as_dict
        return data


class ClusterSerializer(serializers.ModelSerializer):
    display_status = serializers.SerializerMethodField(read_only=True)
    under_task = serializers.SerializerMethodField(read_only=True)
    cluster_template = ClusterTemplateBriefSerializer(read_only=True)
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)

    class Meta:
        model = models.Cluster
        fields = '__all__'

    @staticmethod
    def get_display_status(model):
        return ClusterStatus.choices.get(model.status)

    @staticmethod
    def get_under_task(model):
        if model.status in ClusterStatus.under_progress_statuses:
            return True
        return False
