from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from fleio.openstack.models import Instance

from .models import (OpenStackBackupSchedule, )


class BackupSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenStackBackupSchedule
        fields = ('backup_name', 'backup_type', 'rotation')


class BackupScheduleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    run_at = serializers.DateTimeField(required=True)
    rotation = serializers.IntegerField(allow_null=False, min_value=1, default=1)

    class Meta:
        model = OpenStackBackupSchedule
        fields = ('id', 'instance', 'backup_name', 'backup_type', 'rotation', 'run_at')

    def get_fields(self):
        fields = super().get_fields()
        if 'view' in self.context:
            fields['instance'].queryset = Instance.objects.filter(
                project__service__client__in=self.context['view'].request.user.clients.all()
            )
        return fields

    @staticmethod
    def validate_run_at(backup_date):
        """
        Check that the backup date is not in the past.
        """
        if backup_date < timezone.now():
            msg = _('You cannot do a backup in the past, time travel is not possible, please enter a valid date')
            raise serializers.ValidationError(msg)
        else:
            return backup_date
