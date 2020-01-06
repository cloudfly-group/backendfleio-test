from rest_framework import serializers
from .models import DispatcherLog, NotificationTemplate


class DispatcherLogSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = DispatcherLog
        fields = ('id', 'title', 'generated', 'status')

    @staticmethod
    def get_title(obj):
        return obj.get_title(context={'notification': obj.notification,
                                      'client': obj.notification.client,
                                      'user': obj.notification.user,
                                      'variables': obj.notification.variables})


class DispatcherLogDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    class Meta:
        model = DispatcherLog
        fields = ('id', 'title', 'generated', 'status', 'body')

    @staticmethod
    def get_title(obj):
        return obj.get_title(context={'notification': obj.notification,
                                      'client': obj.notification.client,
                                      'user': obj.notification.user,
                                      'variables': obj.notification.variables})

    @staticmethod
    def get_body(obj):
        return obj.get_body(context={'notification': obj.notification,
                                     'client': obj.notification.client,
                                     'user': obj.notification.user,
                                     'variables': obj.notification.variables})


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ('name', 'content', 'category', 'dispatcher')


class NotificationTemplateOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ('name',)
