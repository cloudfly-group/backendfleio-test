import logging

from django.db import IntegrityError
from django.db.models import ProtectedError
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from fleio.billing.models import Product
from fleio.billing.settings import BillingSettings
from fleio.conf.models import Configuration
from fleio.conf.serializer import ConfSerializer
from fleio.core.drf import FlChoiceField
from fleio.core.drf import ResellerOnly
from fleio.core.exceptions import APIConflict
from fleio.core.models import Client
from fleio.notifications.models import NotificationTemplate
from fleio.reseller.utils import filter_queryset_for_user
from fleio.reseller.utils import user_reseller_resources
from .serializers import ProductWithCyclesSettingsSerializer

LOG = logging.getLogger(__name__)


class BillingSettingsSerializer(ConfSerializer):
    auto_suspend_notification_template = FlChoiceField(choices=NotificationTemplate.objects.choices,
                                                       allow_blank=True, allow_null=True, default='')
    auto_terminate_notification_template = FlChoiceField(choices=NotificationTemplate.objects.choices,
                                                         allow_blank=True, allow_null=True, default='')
    first_credit_notification_template = FlChoiceField(choices=NotificationTemplate.objects.choices,
                                                       allow_blank=True, allow_null=True, default='')
    second_credit_notification_template = FlChoiceField(choices=NotificationTemplate.objects.choices,
                                                        allow_blank=True, allow_null=True, default='')
    third_credit_notification_template = FlChoiceField(choices=NotificationTemplate.objects.choices,
                                                       allow_blank=True, allow_null=True, default='')
    notification_templates = serializers.SerializerMethodField()

    products = serializers.SerializerMethodField()

    class Meta:
        conf_class = BillingSettings
        fields = '__all__'

    @staticmethod
    def get_notification_templates(*args, **kwargs):
        del args, kwargs  # unused
        return NotificationTemplate.objects.unique_choices()

    @staticmethod
    def get_products(*args, **kwargs):
        del args, kwargs  # unused
        return ProductWithCyclesSettingsSerializer(many=True).to_representation(Product.objects.all())


class ConfigurationsSerializer(serializers.ModelSerializer):
    client_count = serializers.SerializerMethodField()
    description = serializers.CharField(required=False, allow_blank=True)

    @staticmethod
    def get_client_count(configuration):
        return Client.objects.filter(configuration=configuration).count()

    class Meta:
        model = Configuration
        fields = '__all__'


class ConfigurationsViewset(viewsets.ModelViewSet):
    serializer_class = ConfigurationsSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    permission_classes = (ResellerOnly,)

    def get_queryset(self):
        return filter_queryset_for_user(Configuration.objects.all(), self.request.user).order_by('name').all()

    def get_serializer_class(self):
        if self.action == 'billing':
            return BillingSettingsSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=['get', 'put'])
    def billing(self, request, pk, *args, **kwargs):
        del pk, args, kwargs  # unused
        configuration = self.get_object()
        conf = BillingSettings(configuration_id=configuration.pk, raise_if_required_not_set=False)
        if request.method == 'GET':
            serializer = BillingSettingsSerializer(instance=conf)
            return Response(serializer.data)
        else:
            serializer = BillingSettingsSerializer(instance=conf, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'detail': _('Settings updated'), 'settings': serializer.data})

    # TODO: make this a generic action to be used by all plugins
    @action(detail=True, methods=['get', 'put'])
    def domains(self, request, pk, *args, **kwargs):
        del pk, args, kwargs  # unused
        try:
            from plugins.domains.configuration import DomainsSettings, DomainsSettingsSerializer
            configuration = self.get_object()
            conf = DomainsSettings(configuration_id=configuration.pk, raise_if_required_not_set=False)
            if request.method == 'GET':
                serializer = DomainsSettingsSerializer(instance=conf)
                return Response(serializer.data)
            else:
                serializer = DomainsSettingsSerializer(instance=conf, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'detail': _('Settings updated'), 'settings': serializer.data})
        except ImportError as e:
            LOG.exception('Cannot load plugin: {}'.format(e))

    # TODO: make this a generic action to be used by all plugins
    @action(detail=True, methods=['get', 'put'])
    def openstack(self, request, pk, *args, **kwargs):
        del pk, args, kwargs  # unused
        try:
            from fleio.openstack.configuration import OpenstackSettings, OpenstackSettingsSerializer
            configuration = self.get_object()
            conf = OpenstackSettings(configuration_id=configuration.pk, raise_if_required_not_set=False)
            if request.method == 'GET':
                serializer = OpenstackSettingsSerializer(instance=conf)
                return Response(serializer.data)
            else:
                serializer = OpenstackSettingsSerializer(instance=conf, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'detail': _('Settings updated'), 'settings': serializer.data})
        except ImportError as e:
            LOG.exception('Cannot load plugin: {}'.format(e))

    def perform_destroy(self, instance: Configuration):
        if instance.is_default:
            raise APIConflict(
                'Unable to delete default configuration {}'.format(instance.name))

        try:
            instance.delete()
        except ProtectedError:
            raise APIConflict(
                'Unable to delete configuration {} while it is assigned to one or more clients'.format(instance.name))

    def perform_create(self, serializer):
        serializer.validated_data['reseller_resources'] = user_reseller_resources(user=self.request.user)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({'name': 'A configuration with this name already exists'})

    def perform_update(self, serializer):
        configuration = self.get_object()
        serializer.validated_data['reseller_resources'] = configuration.reseller_resources
        serializer.save()
