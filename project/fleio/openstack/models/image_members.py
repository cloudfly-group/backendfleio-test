from django.db import models
from django.utils.translation import ugettext_lazy as _


class ImageMemberStatus:
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    choices = (
        (PENDING, _('Pending')),
        (ACCEPTED, _('Accepted')),
        (REJECTED, _('Rejected'))
    )


class ImageMembers(models.Model):
    IMAGE_MEMBER_STATUS = ImageMemberStatus.choices
    image = models.ForeignKey('openstack.Image',
                              db_constraint=False,
                              null=True, blank=True, on_delete=models.DO_NOTHING,
                              related_name='members')
    # NOTE(tomo): Using a FK to Projects forces the images and images members to use tenant/project ownership
    member = models.ForeignKey('openstack.Project', db_constraint=False, null=True, blank=True,
                               on_delete=models.DO_NOTHING, to_field='project_id')
    status = models.CharField(choices=IMAGE_MEMBER_STATUS, max_length=15, default='pending', db_index=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Image members'
