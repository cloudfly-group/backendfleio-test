from django.db import models

from django.utils.translation import ugettext_lazy as _

from fleio.openstack.models import ClusterTemplate


class Cluster(models.Model):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    keypair = models.CharField(max_length=255, null=True, blank=True)
    stack_id = models.CharField(max_length=255, null=True, blank=True)
    master_flavor_id = models.CharField(max_length=255, null=True, blank=True)
    flavor_id = models.CharField(max_length=255, null=True, blank=True)
    health_status = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    status_reason = models.CharField(max_length=1024, null=True, blank=True)
    labels = models.CharField(max_length=1024, blank=True, null=True)
    api_address = models.CharField(max_length=1024, blank=True, null=True)
    discovery_url = models.CharField(max_length=1024, blank=True, null=True)
    node_addresses = models.CharField(max_length=1024, blank=True, null=True)
    master_addresses = models.CharField(max_length=1024, blank=True, null=True)
    cluster_template = models.ForeignKey(
        ClusterTemplate, null=True, blank=True, db_index=True, db_constraint=False, on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        'openstack.Project', db_constraint=False, null=True, blank=True, on_delete=models.SET_NULL,
        to_field='project_id'
    )
    region = models.CharField(max_length=128)
    master_count = models.IntegerField(default=1)
    node_count = models.IntegerField(default=1)
    create_timeout = models.IntegerField(default=60)
    sync_version = models.BigIntegerField(default=0)

    objects = models.Manager

    def __str__(self):
        return self.name if self.name else self.id


class ClusterStatus:
    create_complete = 'CREATE_COMPLETE'
    create_in_progress = 'CREATE_IN_PROGRESS'
    delete_in_progress = 'DELETE_IN_PROGRESS'
    create_failed = 'CREATE_FAILED'
    update_in_progress = 'UPDATE_IN_PROGRESS'
    update_failed = 'UPDATE_FAILED'
    update_complete = 'UPDATE_COMPLETE'
    delete_failed = 'DELETE_FAILED'
    delete_complete = 'DELETE_COMPLETE'
    resume_complete = 'RESUME_COMPLETE'
    resume_failed = 'RESUME_FAILED'
    restore_complete = 'RESTORE_COMPLETE'
    rollback_in_progress = 'ROLLBACK_IN_PROGRESS'
    rollback_failed = 'ROLLBACK_FAILED'
    rollback_complete = 'ROLLBACK_COMPLETE'
    snapshot_complete = 'SNAPSHOT_COMPLETE'
    check_complete = 'CHECK_COMPLETE'
    adopt_complete = 'ADOPT_COMPLETE'

    under_progress_statuses = [create_in_progress, delete_in_progress, update_in_progress, rollback_in_progress]

    choices = {
        create_complete: _('Create completed'),
        create_in_progress: _('Create in progress'),
        delete_in_progress: _('Delete in progress'),
        create_failed: _('Create failed'),
        update_in_progress: _('Update in progress'),
        update_failed: _('Update failed'),
        update_complete: _('Update completed'),
        delete_failed: _('Delete failed'),
        resume_complete: _('Resume completed'),
        resume_failed: _('Resume failed'),
        restore_complete: _('Restore completed'),
        rollback_in_progress: _('Rollback in progress'),
        rollback_failed: _('Rollback failed'),
        rollback_complete: _('Rollback completed'),
        snapshot_complete: _('Snapshot completed'),
        check_complete: _('Check completed'),
        adopt_complete: _('Adopt completed'),
    }
