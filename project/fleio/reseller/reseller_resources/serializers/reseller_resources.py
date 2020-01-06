from rest_framework import serializers

from fleio.reseller.models import ResellerResources


class ResellerResourcesSerializer(serializers.ModelSerializer):
    plan = serializers.SerializerMethodField()

    class Meta:
        model = ResellerResources
        fields = '__all__'

    @staticmethod
    def get_plan(resource: ResellerResources):
        if getattr(resource, 'plan', None):
            return {
                'id': resource.plan.id,
                'name': resource.plan.name
            }
        return None
