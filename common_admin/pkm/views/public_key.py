from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import SuperUserOnly
from fleio.core.filters import CustomFilter
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.pkm.models import PublicKey
from fleio.pkm.serializers import PublicKeySerializer
from fleio.pkm.utils import generate_key_pair
from fleio.pkm.views import PublicKeyViewSet


class AdminPublicKeyViewSet(PublicKeyViewSet):
    permission_classes = (SuperUserOnly,)
    ordering_fields = ('name', 'created_at')
    search_fields = ('name', 'fingerprint')
    filter_backends = (filters.OrderingFilter, CustomFilter, filters.SearchFilter)
    serializer_class = PublicKeySerializer

    @staticmethod
    @action(detail=False, methods=['get'])
    def get_generated_key_pair(request):
        public_key_text, private_key_text = generate_key_pair()
        return Response({'public_key': public_key_text, 'private_key': private_key_text})

    def get_queryset(self):
        return PublicKey.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response
