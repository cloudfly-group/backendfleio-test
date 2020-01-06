import logging

from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import filters
from rest_framework import status as rest_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.billing.models import Product
from fleio.billing.orders.utils import OrderMetadata
from fleio.core.clients.serializers import ClientBriefSerializer
from fleio.core.clients.serializers import ClientSerializer
from fleio.core.clients.serializers import ClientUpdateSerializer
from fleio.core.clients.serializers import CreateClientSerializer
from fleio.core.custom_fields.client_customfield_definition import ClientCustomFieldDefinition
from fleio.core.drf import EndUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import APIConflict
from fleio.core.models import Client
from fleio.core.models import Currency
from fleio.core.signals import client_created
from fleio.core.tasks import complete_signup_task
from fleio.core.utils import get_countries
from fleio.core.validation_utils import validate_services_limit

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='core', object_name='client',
)
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientBriefSerializer
    model = Client
    permission_classes = (EndUserOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'first_name', 'last_name', 'company', 'country', 'city', 'state')

    serializer_map = {'retrieve': ClientSerializer,
                      'create': CreateClientSerializer,
                      'update': ClientUpdateSerializer}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        return self.request.user.clients.all()

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        del request, args, kwargs  # unused
        return Response({'countries': get_countries(),
                         'custom_fields': ClientCustomFieldDefinition().definition,
                         'currencies': [currency.code for currency in Currency.objects.all()]
                         })

    def create(self, request, *args, **kwargs):
        if request.user.clients.count() > 0:  # NOTE(tomo): Removing this should also remove/change the below task
            raise APIConflict(detail=_('Client account already created'), code=rest_status.HTTP_409_CONFLICT)
        resp = super(ClientViewSet, self).create(request=request, *args, **kwargs)
        # First client created. Execute signup task
        # NOTE(tomo): Change this when multi client support is added
        client = request.user.clients.first()
        order_metadata = OrderMetadata.from_request(request=request)
        if client.billing_settings.auto_create_order:
            product_id = client.billing_settings.auto_order_service
            if product_id:
                product = Product.objects.filter(id=product_id).first()
            else:
                product = None
            if product:
                if not validate_services_limit():
                    raise APIBadRequest(
                        _('Cannot create service, please contact support'),
                    )
            transaction.on_commit(lambda: complete_signup_task.delay(
                user_id=request.user.pk,
                client_id=client.pk,
                product_id=product_id,
                order_metadata=order_metadata.to_json(),
            ))
        else:
            LOG.debug('Auto create order on signup disabled')

        return resp

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.validated_data['reseller_resources'] = self.request.user.reseller_resources
                client = serializer.save()
                client.usertoclient_set.create(user=self.request.user, is_client_admin=True)
                client_created.send(sender=self.__class__, client=client)
        except Exception as e:
            LOG.exception(e)
            raise APIBadRequest()

    def destroy(self, request, *args, **kwargs):
        """Does not allow a user to delete his own client"""
        raise MethodNotAllowed(_('Client delete prohibited'))
