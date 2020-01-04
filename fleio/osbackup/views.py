from rest_framework import viewsets
from fleio.core.drf import EndUserOnly
from .models import Instance, OpenStackBackupSchedule
from .serializers import BackupScheduleSerializer


class BackupSchedulesViewSet(viewsets.ModelViewSet):
    serializer_class = BackupScheduleSerializer
    permission_classes = (EndUserOnly,)

    def get_queryset(self):
        related_instances = Instance.objects.filter(project__service__client__in=self.request.user.clients.all())
        return OpenStackBackupSchedule.objects.filter(instance__in=related_instances)
