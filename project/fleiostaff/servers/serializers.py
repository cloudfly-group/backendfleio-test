from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.plugins.plugin_utils import PluginUtils
from fleio.servers.models import HostingServerSettings
from fleio.servers.models import Server
from fleio.servers.models import ServerGroup
from fleio.servers.models.server import ServerStatus

COMPONENT_NAME = 'ServerSettings'


class HostingServerSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostingServerSettings
        exclude = ('server', )


class ServerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerGroup
        fields = '__all__'


class ServerListSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    plugin = serializers.SerializerMethodField()

    class Meta:
        model = Server
        fields = ('id', 'name', 'status', 'created_at', 'group', 'plugin')

    @staticmethod
    def get_group(obj):
        return {'id': obj.group.id, 'name': obj.group.name}

    @staticmethod
    def get_plugin(obj):
        if obj.plugin:
            return {'id': obj.plugin.id, 'label': obj.plugin.app_label}
        else:
            return None


class ServerSerializer(serializers.ModelSerializer):
    settings = serializers.JSONField(required=False, default={})
    plugin_label = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    hosting_server_settings = HostingServerSettingsSerializer(allow_null=True, required=False)

    class Meta:
        model = Server
        fields = '__all__'

    @staticmethod
    def get_plugin_label(obj):
        return obj.plugin.app_label if obj.plugin else None

    @staticmethod
    def get_group_name(obj):
        return obj.group.name

    @staticmethod
    def get_groups(obj):
        return ServerGroup.objects.values('id', 'name')

    def to_representation(self, instance):
        repres = super(ServerSerializer, self).to_representation(instance)
        if instance.plugin:
            component = PluginUtils.get_staff_component(plugin_label=instance.plugin.app_label,
                                                        component_name=COMPONENT_NAME)
            settings_serializer = getattr(component, 'server_settings_serializer', None)
            if settings_serializer:
                context = {'request': self.context.get('request'),
                           'server': instance}
                repres['settings'] = settings_serializer(instance=instance.settings,
                                                         context=context).to_representation(instance.settings)
        return repres

    def to_internal_value(self, data):
        intern = super(ServerSerializer, self).to_internal_value(data)
        plugin = intern.get('plugin')
        if plugin:
            component = PluginUtils.get_staff_component(plugin_label=plugin.app_label,
                                                        component_name=COMPONENT_NAME)
            settings_serializer = getattr(component, 'server_settings_serializer', None)
            if settings_serializer:
                if self.instance:
                    server = self.instance
                else:
                    server = None
                context = {'request': self.context.get('request'),
                           'server': server}
                try:
                    intern['settings'] = settings_serializer(context=context).to_internal_value(intern.get('settings'))
                except ValidationError as v:
                    raise ValidationError(detail={
                        'settings': [v.detail]
                    })
        return intern

    def create(self, validated_data):
        hosting_server_settings = validated_data.pop('hosting_server_settings', None)
        if hosting_server_settings:
            with transaction.atomic():
                server = super(ServerSerializer, self).create(validated_data)
                HostingServerSettings.objects.create(server=server, **hosting_server_settings)
                return server
        else:
            return super(ServerSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        up_hss = validated_data.pop('hosting_server_settings', None)
        if up_hss:
            with transaction.atomic():
                try:
                    hss = instance.hosting_server_settings
                except ObjectDoesNotExist:
                    HostingServerSettings.objects.create(server=instance, **up_hss)
                else:
                    for attr, value in up_hss.items():
                        setattr(hss, attr, value)
                    hss.save()
        return super(ServerSerializer, self).update(instance=instance, validated_data=validated_data)


class ServerDetailSerializer(ServerSerializer):
    has_settings_component = serializers.SerializerMethodField()
    available_groups = serializers.SerializerMethodField()
    available_statuses = serializers.SerializerMethodField()
    available_plugins = serializers.SerializerMethodField()
    plugin_details = serializers.SerializerMethodField()

    @staticmethod
    def get_has_settings_component(obj: Server):
        return PluginUtils.has_staff_component(plugin_label=obj.plugin.app_label,
                                               component_name=COMPONENT_NAME)

    @staticmethod
    def get_available_groups(obj):
        return ServerGroup.objects.values('id', 'name')

    @staticmethod
    def get_available_statuses(obj):
        return ServerStatus.CHOICES

    @staticmethod
    def get_plugin_details(obj):
        if obj.plugin:
            plugin = PluginUtils.get_plugin(config_type='staff', plugin_label=obj.plugin.app_label)
            has_settings_component = PluginUtils.has_component(config_type='staff',
                                                               plugin_label=obj.plugin.app_label,
                                                               component_name='ServerSettings')

            return {'label': obj.plugin.app_label,
                    'id': obj.plugin.id,
                    'display_name': obj.plugin.display_name,
                    'has_settings_component': has_settings_component,
                    'has_server_settings': True,
                    'server_settings': plugin.server_settings
                    }
        else:
            return None

    @staticmethod
    def get_available_plugins(obj):
        return PluginUtils.get_server_plugins()
