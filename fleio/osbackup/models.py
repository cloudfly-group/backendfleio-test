from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from fleio.core.utils import RandomId
from fleio.openstack.models import Instance


@python_2_unicode_compatible
class OpenStackBackupSchedule(models.Model):
    BACKUP_DAILY = 'daily'
    BACKUP_WEEKLY = 'weekly'
    BACKUP_TYPE_CHOICES = ((BACKUP_DAILY, _('Daily')),
                           (BACKUP_WEEKLY, _('Weekly')))

    id = models.BigIntegerField(unique=True, default=RandomId('osbackup.OpenStackBackupSchedule'), primary_key=True)
    instance = models.ForeignKey(Instance, db_constraint=False, related_name='os_backup_schedules',
                                 on_delete=models.CASCADE)
    backup_name = models.CharField(max_length=60)
    backup_type = models.CharField(max_length=10, choices=BACKUP_TYPE_CHOICES)
    rotation = models.IntegerField()
    run_at = models.DateTimeField()

    def __str__(self):
        return self.backup_name


@python_2_unicode_compatible
class OpenStackBackupLog(models.Model):
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Backup - {}".format(self.executed_at.strftime('%Y-%m-%d %H:%M:%S'))
