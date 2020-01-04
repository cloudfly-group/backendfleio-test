from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import ResellerOnly
from fleio.osbilling.models import ServiceDynamicUsage
from fleio.reseller.utils import user_reseller_resources
from reseller.osbilling.service_dynamic_history.serializers.service_dynamic_usage import ServiceDynamicUsageSerializer


class ResellerServiceDynamicUsageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (ResellerOnly,)
    serializer_class = ServiceDynamicUsageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('service__client_id',)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)

        return ServiceDynamicUsage.objects.filter(
            Q(
                service__client__reseller_resources=reseller_resources
            ) | Q(
                reseller_service__client__reseller_resources=reseller_resources
            )
        ).order_by('service__status')

    @action(detail=False, methods=['GET'])
    def client(self, request):
        client_id = request.query_params.get('client_id', None)
        queryset = self.filter_queryset(self.get_queryset()).filter(
            Q(service__client=client_id) | Q(reseller_service__client=client_id)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
