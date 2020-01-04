import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status as rest_status
from rest_framework.decorators import action
from rest_framework.response import Response

import fleio.core.tasks as core_tasks
from common_admin.core.clients.filters import ClientFilter
from common_admin.core.clients.filters import OrderByIdLastFilter
from common_admin.core.clients.views.client import AdminClientViewSet
from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.billing.client_operations import ClientOperations
from fleio.billing.models import Product
from fleio.billing.models import Service
from fleio.billing.modules.factory import module_factory
from fleio.billing.products.serializers import ProductSerializer
from fleio.billing.services.serializers import ServiceBriefSerializer
from fleio.billing.services.serializers import StaffCreateServiceSerializer
from fleio.billing.settings import ProductType
from fleio.billing.settings import ServiceStatus
from fleio.conf.models import Configuration
from fleio.core.drf import CustomPermissions
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import ForbiddenException
from fleio.core.exceptions import ObjectNotFound
from fleio.core.features import staff_active_features
from fleio.core.filters import CustomFilter
from fleio.core.models import Client
from fleio.core.models import ClientGroup
from fleio.core.models import ClientStatus
from fleio.core.models import UserToClient
from fleio.core.serializers import UserMinSerializer
from fleio.openstack.models import Port
from fleio.osbilling.models import PricingPlan
from fleio.reseller.reseller_resources.serializers.reseller_resources import ResellerResourcesSerializer
from fleio.reseller.utils import client_reseller_resources
from fleio.reseller.utils import reseller_suspend_instead_of_terminate
from fleiostaff.core.clients.serializers import BillingAgreementsSetSerializer
from fleiostaff.core.clients.serializers import ChangeCreditSerializer
from fleiostaff.core.clients.serializers import ConfigurationIdSerializer
from fleiostaff.core.clients.serializers import MassEmailSerializer
from fleiostaff.core.clients.serializers import OverdueClientSerializer
from fleiostaff.core.clients.serializers import StaffClientBriefSerializer
from fleiostaff.core.clients.serializers import StaffClientSerializer
from fleiostaff.core.clients.serializers import StaffClientUpdateSerializer
from fleiostaff.core.clients.serializers import StaffCreateClientSerializer
from fleiostaff.core.clients.serializers import UserIdSerializer
from fleiostaff.core.signals import staff_delete_client


@log_staff_activity(
    category_name='core', object_name='client',
    additional_activities={
        'suspend': _('Staff user {username} ({user_id}) suspended client {client_name} ({object_id}).'),
        'resume': _('Staff user {username} ({user_id}) resumed client {client_name} ({object_id}).'),
        'change_credit': _('Staff user {username} ({user_id}) changed credit for client ({object_id}).'),
        'update_usage': _('Staff user {username} ({user_id}) updated usage for client ({object_id}).'),
        'reset_usage': _('Staff user {username} ({user_id}) reset usage for client ({object_id}).'),
        'associate_user': _('Staff user {username} ({user_id}) associated used to client ({object_id}).'),
        'dissociate_user': _('Staff user {username} ({user_id}) dissociated used from client ({object_id}).'),
        'change_configuration': _('Staff user {username} ({user_id}) changed configuration for client ({object_id}).'),
        'add_to_group': _('Staff user {username} ({user_id}) added client ({object_id}) to a group.'),
        'remove_from_group': _('Staff user {username} ({user_id}) removed client ({object_id}) from a group.'),
        'set_billing_agreements': _(
            'Staff user {username} ({user_id}) set billing agreements.'
        ),
        'send_mass_email': _('Staff user {username} ({user_id}) sent mass email to clients.'),
    }
)
class StaffClientViewSet(AdminClientViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
    model = Client
    serializer_class = StaffClientSerializer
    filter_backends = (OrderByIdLastFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_class = ClientFilter
    filter_fields = ('id', 'external_billing_id', 'has_billing_agreement')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'company', 'external_billing_id', 'configuration__name',
                     'groups__name')
    ordering_fields = ('id', 'first_name', 'last_name', 'company', 'address1', 'address2', 'city', 'country',
                       'state', 'date_created', 'uptodate_credit', 'configuration_name', 'group_name')
    serializer_map = {'list': StaffClientBriefSerializer,
                      'create': StaffCreateClientSerializer,
                      'change_credit': ChangeCreditSerializer,
                      'update': StaffClientUpdateSerializer,
                      'associate_user': UserIdSerializer,
                      'dissociate_user': UserIdSerializer}

    queryset = Client.objects.all()

    @action(detail=True, methods=['post'])
    def update_usage(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        ClientOperations(client=client).update_usage()

        return Response({'detail': _('Usage updated')})

    @action(detail=True, methods=['post'])
    def reset_usage(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        ClientOperations(client=client).reset_usage()

        return Response({'detail': _('Usage updated')})

    @action(detail=True, methods=['get'])
    def billing_summary(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        if client.first_project is None:
            return Response({})

        # TODO - #1020: iterate over all services and get usage summary for all
        service = client.first_project.service
        billing_module = module_factory.get_module_instance(service=service)
        summary = billing_module.get_billing_summary(service=service)

        return Response(summary)

    def perform_destroy(self, client):
        activity_helper.add_current_activity_params(client_name=client.name)
        if client.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(client=client):
            return self.suspend(self.request, client.pk)

        client.status = ClientStatus.deleting
        client.save()

        delete_all_resources = (
            self.request.query_params.get('delete_cloud_resources', None) in (
                'true', 'True', '1'
            ) or self.request.data.get(
                'delete_cloud_resources', None
            ) in ('true', 'True', '1')
        )

        user = self.request.user

        core_tasks.terminate_client.delay(
            client_id=client.id,
            user_id=user.id,
            delete_all_resources=delete_all_resources,
        )

        staff_delete_client.send(sender=__name__, user=user, user_id=user.id,
                                 client_name=client.name, client_id=client.id,
                                 username=user.username, request=self.request)

        return Response({'detail': _('Client delete scheduled')}, status=rest_status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def associate_user(self, request, pk):
        del pk  # unused
        client = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=serializer.validated_data['user_id'])
        except user_model.DoesNotExist:
            raise ObjectNotFound({'detail': _('User not found')})
        UserToClient.objects.create(user=user, client=client)
        return Response({'detail': _('User associated')})

    @action(detail=True, methods=['post'])
    def dissociate_user(self, request, pk):
        del pk  # unused
        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        client = self.get_object()
        try:
            # delete the cart related to client
            client_cart = client.fleio_cart
            client_cart.delete()
        except Client.fleio_cart.RelatedObjectDoesNotExist:
            pass
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=serializer.validated_data['user_id'])
            try:
                # delete the cart related to user
                user_cart = user.fleio_cart
                user_cart.delete()
            except user_model.fleio_cart.RelatedObjectDoesNotExist:
                pass
        except user_model.DoesNotExist:
            raise ObjectNotFound({'detail': _('User not found')})
        UserToClient.objects.filter(user=user, client=client).delete()
        return Response({'detail': _('User dissociated')})

    @action(detail=True, methods=['get'])
    def get_users_not_in_client(self, request, pk):
        del request, pk  # unused
        """Retrieve regular active users without any client associated to them"""
        self.get_object()  # Checks permissions
        users = get_user_model().objects.filter(is_active=True, is_staff=False, clients__isnull=True)
        return Response({'users': UserMinSerializer(instance=users, many=True).data})

    @action(detail=True, methods=['get'])
    def get_configurations_for_client(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        configurations = Configuration.objects.filter(
            reseller_resources=client.reseller_resources
        ).exclude(id=client.configuration_id)
        return Response(
            {'configurations': [{'id': config.id, 'name': config.name} for config in configurations]})

    @action(detail=True, methods=['post'])
    def change_configuration(self, request, pk):
        del pk  # unused
        serializer = ConfigurationIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = self.get_object()
        try:
            config = Configuration.objects.get(pk=serializer.validated_data['configuration'])
        except Configuration.DoesNotExist:
            raise ObjectNotFound({'detail': _('Configuration does not exist')})

        client.configuration = config
        client.save(update_fields=['configuration'])

        return Response({'detail': _('Ok')})

    @action(detail=True, methods=['get'])
    def get_cloud_summary(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        if client.first_project is None:
            return Response({})

        # TODO - #1020: iterate over all services and get usage summary for all
        service = client.first_project.service
        billing_module = module_factory.get_module_instance(service=service)
        summary = billing_module.get_usage_summary(service=service)

        return Response(summary)

    @action(detail=True, methods=['get'])
    def get_all_client_ports(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        if client.first_project is None:
            return Response({})

        project = client.first_project
        ports = Port.objects.filter(project_id=project.project_id)
        count = ports.count()
        return Response({
            'name': 'Ports',
            'count': count,
            'load_count': count,
            'objects': [{'id': port.id, 'name': port.name or port.id, 'fixed_ips': port.fixed_ips} for port in ports]
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        del request  # unused
        client_info = {
            'count': Client.objects.count(),
            'new': Client.objects.filter(date_created__gt=utcnow() - datetime.timedelta(days=2)).count()
        }
        return Response(client_info)

    @action(detail=False, methods=['get'])
    def get_available_clients_for_group(self, request):
        group_id = request.query_params.get('group')
        search = request.query_params.get('search')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter clients against it'))
        try:
            group = ClientGroup.objects.get(id=group_id)
        except ClientGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))
        queryset = Client.objects.all()
        queryset = queryset.exclude(groups=group)
        if search:
            queryset = queryset.filter(Q(first_name__contains=search) | Q(last_name__contains=search))
        objects = StaffClientSerializer(instance=queryset, many=True, read_only=True).data
        return Response({'objects': objects})

    @action(detail=False, methods=['get'])
    def get_clients_in_group(self, request):
        group_id = request.query_params.get('group_id')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter clients against it'))
        try:
            group = ClientGroup.objects.get(id=group_id)
        except ClientGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))
        queryset = Client.objects.filter(groups=group)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = StaffClientSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StaffClientSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_group(self, request, pk):
        del pk  # unused

        client = self.get_object()

        group_id = request.data.get('group_id')
        if not group_id:
            raise APIBadRequest(_('Missing group id'))
        try:
            group = ClientGroup.objects.get(id=group_id)
        except ClientGroup.DoesNotExist:
            raise APIBadRequest(_('No group with the provided id found'))

        client.groups.add(group)

        return Response({'detail': _('Client added to group')})

    @action(detail=True, methods=['post'])
    def remove_from_group(self, request, pk):
        del pk  # unused

        client = self.get_object()

        group_id = request.data.get('group_id')
        if not group_id:
            raise APIBadRequest(_('Missing group id'))
        try:
            group = ClientGroup.objects.get(id=group_id)
        except ClientGroup.DoesNotExist:
            raise APIBadRequest(_('No group with the provided id found'))

        client.groups.remove(group)

        return Response({'detail': _('Client removed from group')})

    @action(detail=False, methods=['get'])
    def over_credit_limit(self, request):
        """Return all active clients that should be billed if:
         * the credit limit is negative
         * their current credit is under credit limit
         * they have unsettled openstack billing histories
        """
        del request  # unused

        clients_qs = self.get_queryset().active()  # Get all active clients
        clients_qs = self.filter_queryset(clients_qs)  # Apply any filters, from query params
        serializer = OverdueClientSerializer(clients_qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_billing_agreements(self, request):
        ser = BillingAgreementsSetSerializer(data=request.data, many=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'detail': 'Ok'})

    @action(detail=False, methods=['post'])
    def send_mass_email(self, request):
        mass_email_serializer = MassEmailSerializer(data=request.data)
        if mass_email_serializer.is_valid(raise_exception=True):
            core_tasks.send_mass_email.delay(
                from_name_addr=mass_email_serializer.validated_data['from_name_addr'],
                subject=mass_email_serializer.validated_data['subject'],
                body=mass_email_serializer.validated_data['body'],
                send_batch_size=mass_email_serializer.validated_data['send_batch_size'],
                send_interval=mass_email_serializer.validated_data['send_interval'],
                filtering=mass_email_serializer.validated_data['filter'],
                search=mass_email_serializer.validated_data['search'],
                search_fields=self.search_fields,
                attachments=mass_email_serializer.validated_data['attachments'],
                allowed_variables=self.get_email_variables(),
            )
            return Response({'detail': _('Mass email scheduled')})

    @action(detail=True, methods=['get'])
    def reseller_services(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        services = client.services.filter(
            product__product_type=ProductType.reseller,
            reseller_resources__isnull=False,
        )

        serialized_services = ServiceBriefSerializer(many=True).to_representation(services)
        serialized_resources = {
            service.id: ResellerResourcesSerializer().to_representation(
                service.reseller_resources
            ) for service in services
        }

        return Response({
            'services': serialized_services,
            'resources': serialized_resources,
        })

    @action(detail=True, methods=['post'])
    def create_reseller_service(self, request, pk):
        del pk  # unused

        # TODO - #1019: implement proper creation of service here
        serializer = StaffCreateServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = self.get_object()
        reseller_resources = client_reseller_resources(client=client)

        if reseller_resources is not None:
            raise ForbiddenException({'detail': _('Client already has a reseller service')})

        reseller_product = Product.objects.get(id=serializer.validated_data['product_id'])
        reseller_product_cycle = reseller_product.cycles.filter(id=serializer.validated_data['product_cycle_id'])[0]

        service = Service.objects.create(
            client=client,
            product=reseller_product,
            cycle=reseller_product_cycle,
            display_name='Reseller service',
            status=ServiceStatus.active,
        )

        module_factory.get_module_instance(service=service).create(service=service)

        return Response({'detail': _('Ok')})

    @action(detail=True, methods=['get'])
    def new_reseller_service_data(self, request, pk):
        del request, pk  # unused
        products = Product.objects.filter(
            product_type=ProductType.reseller,
        )

        return Response({
            'products': ProductSerializer(products, many=True).data,
        })

    @action(detail=True, methods=['post'])
    def update_reseller_billing_plan(self, request, pk):
        del pk  # unused
        client = self.get_object()
        plan_id = request.data['plan']
        reseller_service_id = request.data['service']

        try:
            plan = PricingPlan.objects.get(id=plan_id)
        except PricingPlan.DoesNotExist:
            raise ObjectNotFound({'detail': _('Plan not found')})

        try:
            reseller_service = Service.objects.get(id=reseller_service_id)
        except Service.DoesNotExist:
            raise ObjectNotFound({'detail': _('Service not found')})

        reseller_service.reseller_resources.plan = plan
        reseller_service.reseller_resources.save()
        for service in Service.objects.filter(client__reseller_resources=reseller_service.reseller_resources):
            service.reseller_service_dynamic_usage.plan = plan
            service.reseller_service_dynamic_usage.save()

        return Response({'detail': 'Plan updated'})

    @action(detail=True, methods=['post'])
    def update_reseller_enduser_panel_url(self, request, pk):
        del pk  # unused
        client = self.get_object()
        enduser_panel_url = request.data['enduser_panel_url']
        reseller_service_id = request.data['service']

        try:
            reseller_service = Service.objects.get(id=reseller_service_id)
        except Service.DoesNotExist:
            raise ObjectNotFound({'detail': _('Service not found')})

        reseller_service.reseller_resources.enduser_panel_url = enduser_panel_url
        reseller_service.reseller_resources.save()

        return Response({'detail': 'Enduser panel url updated'})
