from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class SecurityGroup(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey('openstack.Project', db_constraint=False, null=True, blank=True,
                                on_delete=models.DO_NOTHING, to_field='project_id')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    region = models.ForeignKey('openstack.OpenstackRegion', db_constraint=False, null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    sync_version = models.BigIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.name or self.id)


@python_2_unicode_compatible
class SecurityGroupRule(models.Model):
    DIRECTIONS = [('ingress', _('Ingress')), ('egress', _('Egress'))]
    id = models.CharField(max_length=36, primary_key=True)
    security_group = models.ForeignKey(SecurityGroup, db_constraint=False, null=True, blank=True,
                                       related_name='security_group_rules', on_delete=models.CASCADE)
    remote_group = models.ForeignKey(SecurityGroup, db_constraint=False, null=True, blank=True,
                                     on_delete=models.DO_NOTHING, related_name='remote_group_rules')
    project = models.ForeignKey('openstack.Project', db_constraint=False, null=True, blank=True,
                                on_delete=models.DO_NOTHING, to_field='project_id')
    description = models.CharField(max_length=255, null=True, blank=True)
    direction = models.CharField(choices=DIRECTIONS, max_length=12)
    protocol = models.CharField(max_length=40, null=True, blank=True)
    ethertype = models.CharField(max_length=40, null=True, blank=True)
    port_range_min = models.IntegerField(null=True, blank=True)
    port_range_max = models.IntegerField(null=True, blank=True)
    remote_ip_prefix = models.CharField(max_length=255, null=True, blank=True)
    revision_number = models.IntegerField(default=1)
    sync_version = models.BigIntegerField(default=0)

    def get_remote_group_name(self):
        try:
            return self.remote_group.name
        except (SecurityGroup.DoesNotExist, AttributeError):
            return ''

    def __str__(self):
        return '{}'.format(self.description or self.id)
