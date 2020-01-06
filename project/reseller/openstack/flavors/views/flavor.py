import logging

from django.utils.translation import ugettext_lazy as _

from django.db.models import Q
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response

from common_admin.openstack.flavors.views.flavor import AdminFlavorViewSet
from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.models import Instance
from fleio.reseller.utils import user_reseller_resources
from reseller.openstack.flavors.serializers.flavor import ResellerFlavorSerializer
from reseller.openstack.flavors.serializers.flavor import ResellerFlavorUpdateSerializer

LOG = logging.getLogger(__name__)


class ResellerFlavorViewSet(AdminFlavorViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)
    serializer_class = ResellerFlavorSerializer
    ordering_fields = [
        'reseller_resources', 'id', 'memory_mb', 'root_gb', 'vcpus', 'name', 'region'
    ]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ResellerFlavorUpdateSerializer
        else:
            return ResellerFlavorSerializer

    @staticmethod
    def get_used_flavors_summary_queryset(user):
        reseller_resources = user_reseller_resources(user=user)
        return Instance.objects.filter(
            project__service__client__reseller_resources=reseller_resources
        ).values('flavor').annotate(
            count=Count('id')
        ).exclude(
            status=InstanceStatus.DELETED
        ).exclude(
            terminated_at__isnull=False
        ).order_by()

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)

        if self.action in ['list', 'retrieve', 'display_for_clients', 'hide_for_clients']:
            queryset = super().get_queryset().filter(
                Q(reseller_resources=reseller_resources) | Q(
                    reseller_resources__isnull=True,
                    show_in_fleio=True,
                    is_public=True,
                    disabled=False,
                ),
            )
        else:
            queryset = super().get_queryset().filter(
                reseller_resources=reseller_resources,
            )

        return queryset.order_by('-reseller_resources', 'memory_mb', 'id')

    @action(detail=True, methods=['post'])
    def display_for_clients(self, request, pk):
        del request, pk  # unused
        flavor = self.get_object()
        reseller_resources = user_reseller_resources(self.request.user)
        flavor.used_by_resellers.add(reseller_resources)
        flavor.save()
        return Response({'detail': _('Flavor will be displayed for clients')})

    @action(detail=True, methods=['post'])
    def hide_for_clients(self, request, pk):
        del request, pk  # unused
        flavor = self.get_object()
        reseller_resources = user_reseller_resources(self.request.user)
        flavor.used_by_resellers.remove(reseller_resources)
        flavor.save()
        return Response({'detail': _('Flavor will be hidden for clients')})
