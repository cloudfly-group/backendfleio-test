from django.db import models
from django.db.models import Count
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField


@python_2_unicode_compatible
class NetworkRbac(models.Model):
    id = models.CharField(max_length=36, unique=True, db_index=True, primary_key=True)
    object_id = models.CharField(max_length=36, db_index=True)
    project_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    target_project = models.CharField(max_length=255, db_index=True)
    action = models.CharField(max_length=255, db_index=True)
    object_type = models.CharField(max_length=255, db_index=True)
    sync_version = models.BigIntegerField(default=0)

    def __str__(self):
        return self.id


class NetworkManager(models.Manager):
    @staticmethod
    def annotate_subnet_count():
        """Add subnet count to each network in a queryset as subnet_count"""
        return {'subnet_count': Count('subnet')}

    def get_networks_for_project(self, project_id, shared=True, external=False, subnet_count=False):
        """Get networks by using the RBAC rules and optionally add
         a subnet_count attribute to each network object.
        :param project_id: str or unicode; the project id to filter by
        :param shared: bool; also returns shared networks owned by other tenants
        :param external: bool; also returns external networks owned by their tenants
        :param subnet_count: add the subnet_count to the model
        """
        if shared or external:
            actions = list()
            if shared:
                actions.append('access_as_shared')
            if external:
                actions.append('access_as_external')
            rbac_filter = NetworkRbac.objects.filter(action__in=actions,
                                                     target_project__in=[project_id, '*'],
                                                     object_type='network')

            filtered = self.filter(models.Q(project=project_id) | models.Q(id__in=rbac_filter.values_list('object_id')))
        else:
            filtered = self.filter(project=project_id)
        if subnet_count:
            return filtered.annotate(**self.annotate_subnet_count())
        else:
            return filtered

    def get_external_networks(self, project_id=None, subnet_count=False):
        """Returns all external networks accessible by the anyone including
         the external networks that are only accessible by the project_id if specified.
        """
        if project_id is not None:
            target_project = [project_id, '*']
        else:
            target_project = ['*']
        rbac_filter = NetworkRbac.objects.filter(action='access_as_external',
                                                 target_project__in=target_project,
                                                 object_type='network')
        filtered = self.filter(id__in=rbac_filter.values_list('object_id'))
        if subnet_count:
            return filtered.annotate(**self.annotate_subnet_count())
        else:
            return filtered


@python_2_unicode_compatible
class Network(models.Model):
    id = models.CharField(max_length=36, unique=True, db_index=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=128, db_index=True)
    project = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    shared = models.BooleanField(default=False, db_index=True)
    router_external = models.BooleanField(default=False, db_index=True)
    is_default = models.BooleanField(default=False, db_index=True)
    status = models.CharField(max_length=32, default='UNKNOWN')
    admin_state_up = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)
    extra = JSONField(default=dict())

    objects = NetworkManager()

    class Meta:
        ordering = ['-created_at']

    @property
    def subnets(self):
        return self.subnet_set.all()

    def __str__(self):
        return "{} - {}".format(self.name, self.description)


class NetworkTag(models.Model):
    tag_name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    network = models.ManyToManyField(Network, db_index=True, related_name='network_tags')

    objects = models.Manager

    def __str__(self):
        return 'Tag "{}" for multiple networks'.format(self.tag_name)
