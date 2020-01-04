from django.db.models import Q
from django.db.models import QuerySet

from fleio.openstack.models import VolumeBackup
from fleio.openstack.models import Volume
from fleio.openstack.volumes.volume_status import VolumeStatus


def has_full_backup_for_incremental_backup(project_id: str, related_volume: Volume) -> bool:
    """Openstack will let a tenant create an incremental backup if a full backup exists on the admin project,
    however it will spawn in error state. Validate if full backup exists in the given project in fleio so further
    problems will be avoided"""
    full_backup = VolumeBackup.objects.filter(
        volume=related_volume, project_id=project_id, is_incremental=False
    ).first()
    if full_backup:
        return True
    return False


def get_volumes_available_for_restoration_queryset(
        search_value: str, backup: VolumeBackup, user_related_clients=None
) -> QuerySet:
    """
    Filters volume available for restoration of a volume backup
    :param search_value: string used for searching volumes by id or name
    :param backup: the volume backup
    :param user_related_clients: clients related to a user for end-user filtering
    :return:
    """
    if user_related_clients:
        queryset = Volume.objects.filter(project__service__client__in=user_related_clients)
    else:
        queryset = Volume.objects.all()
    if search_value:
        filter_param = Q(id__startswith=search_value) | Q(name__istartswith=search_value)
        queryset = queryset.filter(filter_param)
    try:
        backup_related_volume = backup.volume
    except Volume.DoesNotExist:
        pass
    else:
        queryset = queryset.filter(
            region=backup_related_volume.region if backup_related_volume else backup.region, size__gte=backup.size,
            status=VolumeStatus.AVAILABLE
        )
    return queryset
