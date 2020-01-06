from rest_framework import serializers


class TransferDomainSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    epp = serializers.CharField(max_length=256, allow_blank=True, required=False)
    years = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
