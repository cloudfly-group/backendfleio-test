from rest_framework import serializers


class CheckCustomFieldsSerializer(serializers.Serializer):
    contact_type = serializers.ChoiceField(choices=['client', 'contact'])
    domain_name = serializers.CharField(max_length=256, allow_null=False, allow_blank=False)
    client_id = serializers.IntegerField(default=-1, allow_null=True)
    contact_id = serializers.IntegerField(default=-1, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
