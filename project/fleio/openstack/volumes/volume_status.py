from django.utils.translation import ugettext_lazy as _


class VolumeStatus:
    """Volume status mirrored from OpenStack."""
    AVAILABLE = 'available'
    ERROR = 'error'
    EXTENDING = 'extending'
    CREATING = 'creating'
    DELETING = 'deleting'
    IN_USE = 'in-use'
    ATTACHING = 'attaching'
    DETACHING = 'detaching'
    ERROR_DELETING = 'error_deleting'
    MAINTENANCE = 'maintenance'
    RESTORING_BACKUP = 'restoring-backup'

    status_map = {
        AVAILABLE: _('Available'),
        ERROR: _('Error'),
        EXTENDING: _('Extending'),
        CREATING: _('Creating'),
        DELETING: _('Deleting'),
        IN_USE: _('In use'),
        ATTACHING: _('Attaching'),
        DETACHING: _('Detaching'),
        ERROR_DELETING: _('Error deleting'),
        MAINTENANCE: _('Maintenance'),
        RESTORING_BACKUP: _('Restoring backup'),
    }


class VolumeBackupStatus:
    CREATING = 'creating'
    AVAILABLE = 'available'
    DELETING = 'deleting'
    ERROR = 'error'
    RESTORING = 'restoring'
    ERROR_DELETING = 'error_deleting'

    status_map = {
        CREATING: _('Creating'),
        AVAILABLE: _('Available'),
        DELETING: _('Deleting'),
        ERROR: _('Error'),
        RESTORING: _('Restoring'),
        ERROR_DELETING: _('Error deleting'),
    }
