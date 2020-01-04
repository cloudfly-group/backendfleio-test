from rest_framework import viewsets
from fleio.core.drf import StaffOnly
from fleio.osbackup.models import OpenStackBackupSchedule
from fleiostaff.osbackup.serializers import StaffBackupScheduleSerializer


class StaffBackupSchedulesViewSet(viewsets.ModelViewSet):
    serializer_class = StaffBackupScheduleSerializer
    permission_classes = (StaffOnly,)
    queryset = OpenStackBackupSchedule.objects.all()
