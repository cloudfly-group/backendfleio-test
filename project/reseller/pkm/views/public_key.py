from django.db.models import Q

from common_admin.pkm.views.public_key import AdminPublicKeyViewSet
from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import user_reseller_resources
from reseller.pkm.serializers.public_key import ResellerPublicKeySerializer


class ResellerPublicKeyViewSet(AdminPublicKeyViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)
    serializer_class = ResellerPublicKeySerializer

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return super().get_queryset().filter(
            Q(user=self.request.user) | Q(user__reseller_resources=reseller_resources),
        ).all()
