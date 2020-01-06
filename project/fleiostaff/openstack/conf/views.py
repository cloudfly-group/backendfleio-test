from rest_framework.viewsets import ModelViewSet

from fleio.conf.models import Configuration
from fleio.core.drf import StaffOnly
from fleiostaff.conf.views import ConfigurationsSerializer


class OpenstackConfigurationsViewSet(ModelViewSet):
    serializer_class = ConfigurationsSerializer
    permission_classes = (StaffOnly,)
    queryset = Configuration.objects.all()
