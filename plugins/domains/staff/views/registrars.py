from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response

from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest

from plugins.domains.models import Registrar
from plugins.domains.staff.serializers import RegistrarSerializer


class RegistrarsViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly, )
    serializer_class = RegistrarSerializer
    queryset = Registrar.objects.all()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ('name', )
    ordering_fields = ('name', 'created_at')

    def get_serializer(self, *args, **kwargs):
        price_domain_id = self.request.query_params.get(
            'priceDomainId',
            self.request.query_params.get('priceDomainId', None)
        )
        if price_domain_id is not None:
            kwargs['price_domain_id'] = price_domain_id

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        registrar = self.get_object()

        try:
            registrar.delete()
            return Response()
        except IntegrityError:
            raise APIBadRequest(
                detail=_('Cannot delete registrar since it is still in use.')
            )
