from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from fleio.openstack.models import Instance
from fleio.osbackup.models import OpenStackBackupSchedule


class StaffBackupScheduleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    instance = serializers.PrimaryKeyRelatedField(queryset=Instance.objects.all())
    run_at = serializers.DateTimeField(required=True)
    rotation = serializers.IntegerField(allow_null=False, min_value=1, default=1)

    class Meta:
        model = OpenStackBackupSchedule
        fields = ('id', 'instance', 'backup_name', 'backup_type', 'rotation', 'run_at')

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
