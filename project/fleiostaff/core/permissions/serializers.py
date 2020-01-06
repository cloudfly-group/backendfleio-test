from rest_framework import serializers

from django.db import transaction

from fleio.core.models import Permission, PermissionSet


class PermissionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionSet
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id', 'permission_set', 'name', 'granted')
        read_only_fields = ('id', 'permission_set')


class PermissionListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        permission_mapping = {permission.name: permission for permission in instance}
        data_mapping = {item['name']: item for item in validated_data}
        permissions_set = PermissionSet.objects.get(id=self.context.get("permissions_set"))
        # Perform update or create
        ret = []
        with transaction.atomic():
            for permission_name, data in data_mapping.items():
                permission = permission_mapping.get(permission_name, None)
                if permission is None:
                    is_granted = data.pop('granted', None)
                    permission = Permission.objects.create(
                        permission_set=permissions_set,
                        name=permission_name,
                        granted=is_granted
                    )
                    ret.append(self.child.update(permission, data))
                else:
                    ret.append(self.child.update(permission, data))

        return ret


class PermissionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        list_serializer_class = PermissionListSerializer
        fields = ('id', 'name', 'granted')
