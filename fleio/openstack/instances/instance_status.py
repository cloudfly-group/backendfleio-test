from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

DEFAULT_KEY = 'default'


class DisplayStatus(object):
    """Instance status used by Fleio for display purposes."""
    RUNNING = 'Running'
    STOPPED = 'Stopped'
    PAUSED = 'Paused'
    SUSPENDED = 'Suspended'
    ERROR = 'Error'
    REBOOT = 'Reboot'
    HARD_REBOOT = 'Hard Reboot'
    PASSWORD = 'Password'
    REBUILD = 'Rebuild'
    MIGRATING = 'Migrating'
    RESIZE = 'Resize'
    STOPPING = 'Stopping'
    BUILDING = 'Building'
    STARTING = 'Starting'
    VERIFY_RESIZE = 'Verify Resize'
    REVERT_RESIZE = 'Revert Resize'
    RESCUE = 'Rescue'
    RESCUED = 'Rescued'
    BOOTING_FROM_ISO = 'Booting from ISO'
    BOOTED_FROM_ISO = 'Booted from ISO'
    DELETED = 'Deleted'
    SOFT_DELETE = 'Soft Delete'
    SHELVED = 'Shelved'
    SHELVED_OFFLOADED = 'Shelved Offloaded'
    UNKNOWN = 'Unknown'


class InstanceStatus(object):
    """Instance status mirrored from OpenStack."""
    ACTIVE = 'active'  # VM is running
    BUILDING = 'building'  # VM only exists in DB
    PAUSED = 'paused'
    SUSPENDED = 'suspended'  # VM is suspended to disk.
    STOPPED = 'stopped'  # VM is powered off, the disk image is still there.
    RESCUED = 'rescued'  # A rescue image is running with the original VM image attached.
    BOOTED_FROM_ISO = 'booted_from_iso'
    RESIZED = 'resized'  # a VM with the new size is active. The user is expected
    # to manually confirm or revert.

    SOFT_DELETED = 'soft-delete'  # VM is marked as deleted but the disk images are
    # still available to restore.
    DELETED = 'deleted'  # VM is permanently deleted.

    ERROR = 'error'

    SHELVED = 'shelved'  # VM is powered off, resources still on hypervisor
    SHELVED_OFFLOADED = 'shelved_offloaded'  # VM and associated resources are
    # not on hypervisor

    ALLOW_SOFT_REBOOT = [ACTIVE]  # states we can soft reboot from
    ALLOW_HARD_REBOOT = ALLOW_SOFT_REBOOT + [STOPPED, PAUSED, SUSPENDED, ERROR]

    status_map = {
        ACTIVE: _('Active'),
        BUILDING: _('Building'),
        PAUSED: _('Paused'),
        SUSPENDED: _('Suspended'),
        STOPPED: _('Stopped'),
        RESCUED: _('Rescued'),
        RESIZED: _('Resized'),
        BOOTED_FROM_ISO: _('Booted from ISO'),
        SOFT_DELETED: _('Soft delete'),
        DELETED: _('Deleted'),
        ERROR: _('Error'),
        SHELVED: _('Shelved'),
        SHELVED_OFFLOADED: _('Shelved offloaded')
    }


class InstanceTask(object):
    """Instance task state mirrored from OpenStack."""
    # possible task states during create()
    SCHEDULING = 'scheduling'
    BLOCK_DEVICE_MAPPING = 'block_device_mapping'
    NETWORKING = 'networking'
    SPAWNING = 'spawning'

    # possible task states during snapshot()
    IMAGE_SNAPSHOT = 'image_snapshot'
    IMAGE_SNAPSHOT_PENDING = 'image_snapshot_pending'
    IMAGE_PENDING_UPLOAD = 'image_pending_upload'
    IMAGE_UPLOADING = 'image_uploading'

    # possible task states during backup()
    IMAGE_BACKUP = 'image_backup'

    # possible task states during set_admin_password()
    UPDATING_PASSWORD = 'updating_password'

    # possible task states during resize()
    RESIZE_PREP = 'resize_prep'
    RESIZE_MIGRATING = 'resize_migrating'
    RESIZE_MIGRATED = 'resize_migrated'
    RESIZE_FINISH = 'resize_finish'

    # possible task states during revert_resize()
    RESIZE_REVERTING = 'resize_reverting'

    # possible task states during confirm_resize()
    RESIZE_CONFIRMING = 'resize_confirming'

    # possible task states during reboot()
    REBOOTING = 'rebooting'
    REBOOT_PENDING = 'reboot_pending'
    REBOOT_STARTED = 'reboot_started'
    REBOOTING_HARD = 'rebooting_hard'
    REBOOT_PENDING_HARD = 'reboot_pending_hard'
    REBOOT_STARTED_HARD = 'reboot_started_hard'

    # possible task states during pause()
    PAUSING = 'pausing'

    # possible task states during unpause()
    UNPAUSING = 'unpausing'

    # possible task states during suspend()
    SUSPENDING = 'suspending'

    # possible task states during resume()
    RESUMING = 'resuming'

    # possible task states during power_off()
    POWERING_OFF = 'powering-off'

    # possible task states during power_on()
    POWERING_ON = 'powering-on'

    # possible task states during rescue()
    RESCUING = 'rescuing'

    # possible task states during boot from ISO
    BOOTING_FROM_ISO = 'booting_from_iso'

    # possible task states during unrescue()
    UNRESCUING = 'unrescuing'

    # possible task states during unmount ISO
    UNMOUNTING_AND_REBOOTING = 'unmounting_ISO_and_rebooting'

    # possible task states during rebuild()
    REBUILDING = 'rebuilding'
    REBUILD_BLOCK_DEVICE_MAPPING = "rebuild_block_device_mapping"
    REBUILD_SPAWNING = 'rebuild_spawning'

    # possible task states during live_migrate()
    MIGRATING = "migrating"

    # possible task states during delete()
    DELETING = 'deleting'

    # possible task states during soft_delete()
    SOFT_DELETING = 'soft-deleting'

    # possible task states during restore()
    RESTORING = 'restoring'

    # possible task states during shelve()
    SHELVING = 'shelving'
    SHELVING_IMAGE_PENDING_UPLOAD = 'shelving_image_pending_upload'
    SHELVING_IMAGE_UPLOADING = 'shelving_image_uploading'

    # possible task states during shelve_offload()
    SHELVING_OFFLOADING = 'shelving_offloading'

    # possible task states during unshelve()
    UNSHELVING = 'unshelving'

    task_state_filtering_opts_map = {
        SCHEDULING: _('Scheduling'),
        BLOCK_DEVICE_MAPPING: _('Block device mapping'),
        NETWORKING: _('Networking'),
        SPAWNING: _('Spawning'),
        IMAGE_SNAPSHOT: _('Image snapshot'),
        IMAGE_SNAPSHOT_PENDING: _('Image snapshot pending'),
        IMAGE_PENDING_UPLOAD: _('Image pending upload'),
        IMAGE_UPLOADING: _('Image uploading'),
        IMAGE_BACKUP: _('Image backup'),
        UPDATING_PASSWORD: _('Updating password'),
        RESIZE_PREP: _('Resize prep'),
        RESIZE_MIGRATING: _('Resize migrating'),
        RESIZE_MIGRATED: _('Resize migrated'),
        RESIZE_FINISH: _('Resize finish'),
        RESIZE_REVERTING: _('Resize reverting'),
        RESIZE_CONFIRMING: _('Resize confirming'),
        REBOOTING: _('Rebooting'),
        REBOOT_PENDING: _('Reboot pending'),
        REBOOT_STARTED: _('Reboot started'),
        REBOOTING_HARD: _('Rebooting hard'),
        REBOOT_PENDING_HARD: _('Reboot pending hard'),
        REBOOT_STARTED_HARD: _('Reboot started hard'),
        PAUSING: _('Pausing'),
        UNPAUSING: _('Unpausing'),
        SUSPENDING: _('Suspending'),
        RESUMING: _('Resuming'),
        POWERING_OFF: _('Powering off'),
        POWERING_ON: _('Powering on'),
        RESCUING: _('Rescuing'),
        BOOTING_FROM_ISO: _('Booting from ISO'),
        UNRESCUING: _('Unrescuing'),
        UNMOUNTING_AND_REBOOTING: _('Unmounting IOS and rebooting'),
        REBUILDING: _('Rebuilding'),
        REBUILD_BLOCK_DEVICE_MAPPING: _('Rebuild block device mapping'),
        REBUILD_SPAWNING: _('Rebuild spawning'),
        MIGRATING: _('Migrating'),
        DELETING: _('Deleting'),
        SOFT_DELETING: _('Soft deleting'),
        RESTORING: _('Restoring'),
        SHELVING: _('Shelving'),
        SHELVING_IMAGE_PENDING_UPLOAD: _('Shelving image pending upload'),
        SHELVING_IMAGE_UPLOADING: _('Shelving image uploading'),
        SHELVING_OFFLOADING: _('Shelving offloading'),
        UNSHELVING: _('Unshelving'),
    }


INSTANCE_STATE_MAP = {
    InstanceStatus.ACTIVE: {
        DEFAULT_KEY: DisplayStatus.RUNNING,
        InstanceTask.REBOOTING: DisplayStatus.REBOOT,
        InstanceTask.REBOOT_PENDING: DisplayStatus.REBOOT,
        InstanceTask.REBOOT_STARTED: DisplayStatus.REBOOT,
        InstanceTask.REBOOTING_HARD: DisplayStatus.HARD_REBOOT,
        InstanceTask.REBOOT_STARTED_HARD: DisplayStatus.HARD_REBOOT,
        InstanceTask.UPDATING_PASSWORD: DisplayStatus.PASSWORD,
        InstanceTask.REBUILDING: DisplayStatus.REBUILD,
        InstanceTask.REBUILD_BLOCK_DEVICE_MAPPING: DisplayStatus.REBUILD,
        InstanceTask.REBUILD_SPAWNING: DisplayStatus.REBUILD,
        InstanceTask.MIGRATING: DisplayStatus.MIGRATING,
        InstanceTask.RESIZE_PREP: DisplayStatus.RESIZE,
        InstanceTask.RESIZE_MIGRATING: DisplayStatus.RESIZE,
        InstanceTask.RESIZE_MIGRATED: DisplayStatus.RESIZE,
        InstanceTask.RESIZE_FINISH: DisplayStatus.RESIZE,
        InstanceTask.POWERING_OFF: DisplayStatus.STOPPING,
        InstanceTask.RESCUING: DisplayStatus.RESCUE,
        InstanceTask.BOOTING_FROM_ISO: DisplayStatus.BOOTING_FROM_ISO,
    },
    InstanceStatus.BUILDING: {DEFAULT_KEY: DisplayStatus.BUILDING},
    InstanceStatus.STOPPED: {DEFAULT_KEY: DisplayStatus.STOPPED,
                             InstanceTask.RESIZE_PREP: DisplayStatus.RESIZE,
                             InstanceTask.RESIZE_MIGRATING: DisplayStatus.RESIZE,
                             InstanceTask.RESIZE_MIGRATED: DisplayStatus.RESIZE,
                             InstanceTask.RESIZE_FINISH: DisplayStatus.RESIZE,
                             InstanceTask.POWERING_ON: DisplayStatus.STARTING
                             },
    InstanceStatus.RESIZED: {DEFAULT_KEY: DisplayStatus.VERIFY_RESIZE,
                             InstanceTask.RESIZE_REVERTING: DisplayStatus.REVERT_RESIZE
                             },
    InstanceStatus.PAUSED: {DEFAULT_KEY: DisplayStatus.PAUSED},
    InstanceStatus.SUSPENDED: {DEFAULT_KEY: DisplayStatus.SUSPENDED},
    InstanceStatus.RESCUED: {DEFAULT_KEY: DisplayStatus.RESCUED},
    InstanceStatus.BOOTED_FROM_ISO: {DEFAULT_KEY: DisplayStatus.BOOTED_FROM_ISO},
    InstanceStatus.ERROR: {DEFAULT_KEY: DisplayStatus.ERROR},
    InstanceStatus.DELETED: {DEFAULT_KEY: DisplayStatus.DELETED},
    InstanceStatus.SOFT_DELETED: {DEFAULT_KEY: DisplayStatus.SOFT_DELETE},
    InstanceStatus.SHELVED: {DEFAULT_KEY: DisplayStatus.SHELVED},
    InstanceStatus.SHELVED_OFFLOADED: {DEFAULT_KEY: DisplayStatus.SHELVED_OFFLOADED},
    'unknown': {DEFAULT_KEY: DisplayStatus.UNKNOWN}
}


class InstancePowerState(object):
    NO_STATE = 0
    RUNNING = 1
    BLOCKED = 2
    PAUSED = 3
    SHUTDOWN = 4
    SHUTOFF = 5
    CRASHED = 6
    SUSPENDED = 7
    FAILED = 8
    BUILDING = 9
