from rest_framework import serializers

from common_admin.openstack.flavorgroups.serializers import AdminFlavorGroupMinSerializer
from fleio.openstack.models import OpenstackInstanceFlavor
from fleiostaff.core.clientgroups.serializers import ClientGroupsMinSerializer


class FlavorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=36, default='auto')
    flavor_group = AdminFlavorGroupMinSerializer(required=False)
    show_to_groups = ClientGroupsMinSerializer(many=True, read_only=True)
    display_name = serializers.SerializerMethodField()

    @staticmethod
    def get_display_name(flavor: OpenstackInstanceFlavor):
        return '{} ({})'.format(flavor.name, flavor.region.id)

    class Meta:
        model = OpenstackInstanceFlavor
        exclude = ('used_by_resellers', )
        read_only_fields = (
            'vcpu_weight', 'rxtx_factor', 'deleted', 'disabled', 'flavor_group',
            'show_to_groups', 'properties',
        )


class FlavorUpdateSerializer(serializers.ModelSerializer):
    preserve_id = serializers.BooleanField(default=False, required=False, allow_null=False)

    class Meta:
        model = OpenstackInstanceFlavor
        exclude = ('show_to_groups', 'region', 'used_by_resellers')
        read_only_fields = ('id', 'vcpu_weight', 'rxtx_factor', 'deleted', 'disabled', 'flavor_group')
