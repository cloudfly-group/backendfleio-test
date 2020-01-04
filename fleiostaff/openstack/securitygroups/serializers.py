from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.models import Client
from fleio.openstack.models import Instance
from fleio.openstack.models import Port
from fleio.openstack.models import SecurityGroup
from fleio.openstack.networking.serializers import SecurityGroupCreateSerializer
from fleio.openstack.networking.serializers import SecurityGroupRuleSerializer


class StaffSecurityGroupSerializer(serializers.ModelSerializer):
    associated_instances = serializers.SerializerMethodField()
    project = serializers.CharField(source='project_id', read_only=True)

    class Meta:
        model = SecurityGroup
        exclude = ('sync_version',)
        read_only_fields = ('associated_instances', 'project')

    @staticmethod
    def get_associated_instances(security_group):
        device_ids = Port.objects.filter(security_groups__contains=security_group.id).values_list('device_id')
        return Instance.objects.filter(id__in=device_ids).values('id', 'name')


class StaffSecurityGroupCreateSerializer(SecurityGroupCreateSerializer):
    client = serializers.IntegerField(required=False)

    class Meta:
        model = SecurityGroup
        fields = ('id', 'name', 'description', 'region', 'client')
        read_only_fields = ('id',)

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffSecurityGroupCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if 'client' in value:
            client_id = data['client']
            client = Client.objects.filter(id=client_id).first()
            if not client:
                raise ValidationError({'detail': _('No client found.')})
            project = client.first_project
            if not project:
                raise ValidationError({'detail': _('Client has no project.')})
            value['project_id'] = project.project_id
            value.pop('client')

        return value


class StaffSecurityGroupDetailSerializer(serializers.ModelSerializer):
    associated_instances = serializers.SerializerMethodField()
    security_group_rules = SecurityGroupRuleSerializer(many=True)
    project = serializers.CharField(source='project_id', read_only=True)

    class Meta:
        model = SecurityGroup
        read_only_fields = ('associated_instances', 'security_group_rules', 'project')
        exclude = ('sync_version',)

    @staticmethod
    def get_associated_instances(security_group):
        device_ids = Port.objects.filter(security_groups__contains=security_group.id).values_list('device_id')
        instances = Instance.objects.filter(id__in=device_ids)
        return [{'id': instance.id, 'name': instance.name} for instance in instances] if instances else []
