from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import EndUserOnly
from fleio.core.filters import CustomFilter
from fleio.core.permissions.permissions_cache import permissions_cache
from .models import PublicKey
from .serializers import PublicKeySerializer
from .utils import generate_key_pair


class PublicKeyViewSet(viewsets.ModelViewSet):
    serializer_class = PublicKeySerializer
    permission_classes = (EndUserOnly, )
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('name', 'fingerprint')
    ordering_fields = ('name', 'created_at')

    @staticmethod
    @action(detail=False, methods=['get'])
    def get_generated_key_pair(request):
        public_key_text, private_key_text = generate_key_pair()
        return Response({'public_key': public_key_text, 'private_key': private_key_text})

    def get_queryset(self):
        return PublicKey.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
