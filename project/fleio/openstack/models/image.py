from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.openstack.models import FlavorGroup
from fleio.openstack.models import OpenstackInstanceFlavor


class OpenStackImageType:
    TEMPLATE = 'template'
    APPLICATION = 'application'
    SNAPSHOT = 'snapshot'
    BACKUP = 'backup'
    DELETED = 'deleted'

    CHOICES = (
        ('template', _('Template')),
        ('application', _('Application')),
        ('snapshot', _('Snapshot')),
        ('backup', _('Backup')),
        ('deleted', _('Deleted')),
    )


class OpenStackImageVisibility:
    PRIVATE = 'private'
    PUBLIC = 'public'
    SHARED = 'shared'
    COMMUNITY = 'community'

    CHOICES = (
        (PRIVATE, _('Private')),
        (PUBLIC, _('Public')),
        (SHARED, _('Shared')),
        (COMMUNITY, _('Community')),
    )

    @staticmethod
    def get_user_choices(include_public=False, include_community=True):
        choices_list = [OpenStackImageVisibility.PRIVATE, OpenStackImageVisibility.SHARED]
        if include_community:
            choices_list.append(OpenStackImageVisibility.COMMUNITY)
        if include_public:
            choices_list.append(OpenStackImageVisibility.PUBLIC)
        return choices_list

    CHOICE_LIST = (PRIVATE, PUBLIC, SHARED, COMMUNITY)


class OpenStackImageStatus:
    QUEUED = 'queued'
    SAVING = 'saving'
    ACTIVE = 'active'
    KILLED = 'killed'
    DELETED = 'deleted'
    PENDING_DELETE = 'pending_delete'
    DEACTIVATED = 'deactivated'

    CHOICES = (
        (QUEUED, _('Queued')),
        (SAVING, _('Saving')),
        (ACTIVE, _('Active')),
        (KILLED, _('Killed')),
        (DELETED, _('Deleted')),
        (PENDING_DELETE, _('Pending delete')),
        (DEACTIVATED, _('Deactivated'))
    )


class ImageQueryset(models.QuerySet):
    def public(self):
        """Active and public images"""
        return self.filter(status=OpenStackImageStatus.ACTIVE, visibility=OpenStackImageVisibility.PUBLIC)

    def get_images_for_project(self, project_id):
        """
        Returns all images visible by the project that can usually be filtered further by
        region_id and other meaningful attributes.
        """
        return self.filter(models.Q(project_id=project_id) |
                           models.Q(visibility__in=['public', 'community']) |
                           models.Q(visibility='shared',
                                    members__member_id=project_id,
                                    members__status__in=('accepted', 'pending'))).distinct()


@python_2_unicode_compatible
class Image(models.Model):
    IMAGE_STATUS = OpenStackImageStatus.CHOICES
    IMAGE_TYPE = OpenStackImageType.CHOICES
    IMAGE_VISIBILITY = OpenStackImageVisibility.CHOICES
    IMAGE_CONTAINER_FORMAT = (
        ('ami', 'ami'),
        ('ari', 'ari'),
        ('aki', 'aki'),
        ('bare', 'bare'),
        ('ovf', 'ovf'),
        ('ova', 'ova'),
        ('docker', 'docker'),
    )
    IMAGE_DISK_FORMAT = (
        ('ami', 'ami'),
        ('ari', 'ari'),
        ('aki', 'aki'),
        ('vhd', 'vhd'),
        ('vmdk', 'vmdk'),
        ('raw', 'raw'),
        ('qcow2', 'qcow2'),
        ('vdi', 'vdi'),
        ('iso', 'iso'),
    )

    id = models.CharField(max_length=36, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=11, choices=IMAGE_TYPE, default='template', db_index=True)
    region = models.ForeignKey('openstack.OpenstackRegion', db_constraint=False, null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    owner = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=14, choices=IMAGE_STATUS, blank=True, null=True, db_index=True)
    size = models.BigIntegerField(blank=True, null=True)
    virtual_size = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    os_distro = models.CharField(max_length=30, blank=True, null=True, default=None)
    hypervisor_type = models.CharField(max_length=32, blank=True, null=True, default=None)
    os_version = models.CharField(max_length=16, blank=True, null=True)
    architecture = models.CharField(max_length=32, blank=True, null=True)
    min_disk = models.IntegerField(null=False)
    min_ram = models.IntegerField(null=False)
    protected = models.BooleanField(default=False)
    visibility = models.CharField(max_length=10, choices=IMAGE_VISIBILITY, blank=True, null=True, db_index=True)
    container_format = models.CharField(max_length=10, choices=IMAGE_CONTAINER_FORMAT, blank=True, null=True)
    disk_format = models.CharField(max_length=10, choices=IMAGE_DISK_FORMAT, blank=True, null=True)
    properties = JSONField(default=dict())
    tags = JSONField(default=list())
    hw_qemu_guest_agent = models.BooleanField(default=False)
    project = models.ForeignKey('openstack.Project', db_constraint=False, null=True, blank=True,
                                on_delete=models.DO_NOTHING, to_field='project_id')
    # Defined only for snapshots
    instance_uuid = models.CharField(max_length=36, null=True, blank=True)
    volume_snapshot_uuid = models.CharField(max_length=36, null=True, blank=True)
    sync_version = models.BigIntegerField(default=0)
    flavor_groups = models.ManyToManyField(FlavorGroup, related_name='images', blank=True)
    flavors = models.ManyToManyField(OpenstackInstanceFlavor, related_name='images', blank=True)

    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='images',
        default=None,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Images'
        ordering = ['-created_at']

    objects = ImageQueryset.as_manager()

    def __str__(self):
        return self.name or self.id

    @property
    def has_flavors_assigned(self) -> bool:
        return self.flavors.count() + self.flavor_groups.count() != 0
