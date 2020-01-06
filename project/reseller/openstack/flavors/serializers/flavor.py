from rest_framework import serializers

from common_admin.openstack.flavorgroups.serializers import AdminFlavorGroupMinSerializer
from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.core.clientgroups.serializers import ClientGroupsMinSerializer
from reseller.utils.serialization import CurrentResellerResourcesDefault


class ResellerFlavorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=36, default='auto')
    flavor_group = AdminFlavorGroupMinSerializer(required=False)
    show_to_groups = ClientGroupsMinSerializer(many=True, read_only=True)
    display_name = serializers.SerializerMethodField()
    display_for_clients = serializers.SerializerMethodField()

    class Meta:
        model = OpenstackInstanceFlavor
        fields = (
            'id', 'flavor_group', 'show_to_groups', 'display_name', 'name', 'description',
            'memory_mb', 'vcpus', 'swap', 'vcpu_weight', 'rxtx_factor', 'root_gb', 'ephemeral_gb',
            'disabled', 'is_public', 'deleted', 'show_in_fleio', 'out_of_stock', 'properties',
            'region', 'reseller_resources', 'display_for_clients',
        )
        read_only_fields = (
            'vcpu_weight', 'rxtx_factor', 'deleted', 'disabled', 'flavor_group', 'show_to_groups',
            'properties', 'display_for_clients', 'used_by_resellers',
        )

    @staticmethod
    def get_display_name(flavor: OpenstackInstanceFlavor):
        return '{} ({})'.format(flavor.name, flavor.region.id)

    def get_display_for_clients(self, flavor: OpenstackInstanceFlavor):
        reseller_resources = user_reseller_resources(self.context['request'].user)
        if flavor.used_by_resellers.filter(id=reseller_resources.id).first():
            return True
        else:
            return False

    def create(self, validated_data):
        reseller_resources = user_reseller_resources(user=self.context['request'].user)
        validated_data['reseller_resources'] = reseller_resources
        return super().create(validated_data=validated_data)


class ResellerFlavorUpdateSerializer(serializers.ModelSerializer):
    preserve_id = serializers.BooleanField(default=False, required=False, allow_null=False)
    reseller_resources = serializers.HiddenField(default=CurrentResellerResourcesDefault())

    class Meta:
        model = OpenstackInstanceFlavor
        exclude = ('show_to_groups', 'region')
        read_only_fields = (
            'id', 'vcpu_weight', 'rxtx_factor', 'deleted', 'disabled', 'flavor_group',
            'used_by_resellers',
        )
