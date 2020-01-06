from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from fleio.billing.models import ProductGroup
from fleio.core.drf import StaffOnly
from fleiostaff.billing.products.serializers import StaffProductGroupAllSerializer, StaffProductGroupSerializer


class StaffProductGroupViewset(viewsets.ModelViewSet):
    serializer_class = StaffProductGroupAllSerializer
    serializer_map = {'create': StaffProductGroupSerializer,
                      'update': StaffProductGroupSerializer,
                      'retrieve': StaffProductGroupSerializer}
    model = ProductGroup
    queryset = ProductGroup.objects.filter(visible=True).all()
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('id', 'name', 'description')
    ordering_fields = ('name', 'description')
    search_fields = ('name', 'description', 'products__name', 'products__description')
    ordering = ['name']

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)
