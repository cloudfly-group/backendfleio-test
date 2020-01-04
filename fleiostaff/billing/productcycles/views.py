from __future__ import unicode_literals

import logging

from django.db.models import ProtectedError
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.billing.models import Product, ProductCycle
from fleio.billing.settings import CyclePeriods, PricingModel, PublicStatuses
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest, APIConflict, ObjectNotFound
from fleio.core.models import Currency
from fleio.core.serializers import CurrencySerializer
from .serializers import StaffProductCycleSerializer

LOG = logging.getLogger(__name__)


class StaffProductCycleViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = StaffProductCycleSerializer

    def get_queryset(self):
        return ProductCycle.objects.all().order_by('pk')

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product')  # type: Product
        if product.price_model == PricingModel.free:
            raise APIBadRequest(_('Cannot add cycle to a free product.'))
        serializer.save()

    @action(detail=False, methods=['GET'])
    def create_options(self, request):
        options = dict()
        options['products'] = [{'id': pack.id, 'name': pack.name, 'description': pack.description}
                               for pack in Product.objects.all()]
        if not options['products']:
            raise ObjectNotFound('No products exist')
        options['cycles'] = CyclePeriods.choices
        options['currencies'] = CurrencySerializer(instance=Currency.objects.all(), many=True).data
        if not options['currencies']:
            raise ObjectNotFound('No currencies exist')
        options['statuses'] = PublicStatuses.choices
        return Response({'create_options': options})

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            # TODO(erno): maybe return the objects which reference the cycles (exception.protected_objects)
            raise APIConflict(_("Can't delete cycle. It is referenced by another object"))
