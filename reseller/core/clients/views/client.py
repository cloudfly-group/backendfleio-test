import datetime

from django.contrib.auth import get_user_model
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status as rest_status
from rest_framework.decorators import action
from rest_framework.response import Response

from common_admin.core.clients.filters import ClientFilter
from common_admin.core.clients.filters import OrderByIdLastFilter
from common_admin.core.clients.views.client import AdminClientViewSet
from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.conf.models import Configuration
from fleio.core import tasks as core_tasks
from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.core.exceptions import ForbiddenException
from fleio.core.exceptions import ObjectNotFound
from fleio.core.features import reseller_active_features
from fleio.core.filters import CustomFilter
from fleio.core.models import Client
# TODO: remove fleiostaff dependencies
from fleio.core.models import ClientStatus
from fleio.core.models import UserToClient
from fleio.core.serializers import UserMinSerializer
from fleio.reseller.utils import filter_queryset_for_user
from fleio.reseller.utils import reseller_suspend_instead_of_terminate
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.core.clients.serializers import ChangeCreditSerializer
from fleiostaff.core.clients.serializers import ConfigurationIdSerializer
from fleiostaff.core.clients.serializers import StaffClientBriefSerializer
from fleiostaff.core.clients.serializers import StaffClientSerializer
from fleiostaff.core.clients.serializers import StaffCreateClientSerializer
from fleiostaff.core.clients.serializers import UserIdSerializer
from reseller.core.clients.serializers.client import ResellerClientUpdateSerializer
from reseller.core.signals import reseller_delete_client


@log_reseller_activity(
    category_name='core', object_name='client',
    additional_activities={
        'suspend': _('Reseller user {username} ({user_id}) suspended client {client_name} ({object_id}).'),
        'resume': _('Reseller user {username} ({user_id}) resumed client {client_name} ({object_id}).'),
        'change_credit': _('Reseller user {username} ({user_id}) changed credit for client ({object_id}).'),
        'update_usage': _('Reseller user {username} ({user_id}) updated usage for client ({object_id}).'),
        'reset_usage': _('Reseller user {username} ({user_id}) reset usage for client ({object_id}).'),
        'associate_user': _('Reseller user {username} ({user_id}) associated used to client ({object_id}).'),
        'dissociate_user': _('Reseller user {username} ({user_id}) dissociated used from client ({object_id}).'),
        'change_configuration': _(
            'Reseller user {username} ({user_id}) changed configuration for client ({object_id}).'
        ),
        'update_openstack_billing_plan': _(
            'Reseller user {username} ({user_id}) updated openstack billing plan for client ({object_id}).'
        ),
        'add_to_group': _('Reseller user {username} ({user_id}) added client ({object_id}) to a group.'),
        'remove_from_group': _('Reseller user {username} ({user_id}) removed client ({object_id}) from a group.'),
        'set_billing_agreements': _(
            'Reseller user {username} ({user_id}) set billing agreements.'
        ),
        'send_mass_email': _('Reseller user {username} ({user_id}) sent mass email to clients.'),
    }
)
class ResellerClientViewSet(AdminClientViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)
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
                      'update': ResellerClientUpdateSerializer,
                      'associate_user': UserIdSerializer,
                      'dissociate_user': UserIdSerializer}

    queryset = Client.objects.all()

    def get_queryset(self):
        return filter_queryset_for_user(super().get_queryset(), self.request.user).all()

    def perform_create(self, serializer):
        serializer.validated_data['reseller_resources'] = user_reseller_resources(user=self.request.user)
        serializer.save()

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
        if reseller_active_features.is_enabled('demo'):
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
        del pk  # unused
        """Retrieve regular active users without any client associated to them"""
        self.get_object()  # Checks permissions
        reseller_resources = user_reseller_resources(request.user)
        users = get_user_model().objects.filter(
            is_active=True,
            is_staff=False,
            is_reseller=False,
            clients__isnull=True,
            reseller_resources=reseller_resources,
        )
        return Response({'users': UserMinSerializer(instance=users, many=True).data})

    @action(detail=True, methods=['get'])
    def get_configurations_for_client(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        reseller_resources = user_reseller_resources(self.request.user)
        configurations = Configuration.objects.filter(
            reseller_resources=reseller_resources
        ).exclude(id=client.configuration_id)
        return Response(
            {'configurations': [{'id': config.id, 'name': config.name} for config in configurations]})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        del request  # unused
        reseller_resources = user_reseller_resources(self.request.user)
        client_info = {
            'count': Client.objects.filter(reseller_resources=reseller_resources).count(),
            'new': Client.objects.filter(
                date_created__gt=utcnow() - datetime.timedelta(days=2),
                reseller_resources=reseller_resources
            ).count()
        }
        return Response(client_info)

    @action(detail=True, methods=['post'])
    def change_configuration(self, request, pk):
        del pk  # unused
        serializer = ConfigurationIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = self.get_object()
        reseller_resources = user_reseller_resources(self.request.user)
        try:
            config = Configuration.objects.get(
                pk=serializer.validated_data['configuration'],
                reseller_resources=reseller_resources,
            )
        except Configuration.DoesNotExist:
            raise ObjectNotFound({'detail': _('Configuration does not exist')})

        client.configuration = config
        client.save(update_fields=['configuration'])

        return Response({'detail': _('Ok')})

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

        reseller_delete_client.send(
            sender=__name__, user=user, user_id=user.id,
            client_name=client.name, client_id=client.id,
            username=user.username, request=self.request
        )

        return Response({'detail': _('Client delete scheduled')}, status=rest_status.HTTP_202_ACCEPTED)
