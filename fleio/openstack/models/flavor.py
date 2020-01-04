import decimal

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from fleio.core.models import Client
from fleio.core.models import ClientGroup
from fleio.openstack.models.flavorgroup import FlavorGroup


class FlavorManager(models.Manager):
    def get_for_project(self, project_id, **kwargs):
        """
        Get all flavors available for a project
        This function also filters by client groups, if the project has a client and
        the client is a member of one or more groups.
        """
        flavors = self.filter(is_public=True)
        try:
            client = Client.objects.get(services__openstack_project__project_id=project_id)
        except (Client.DoesNotExist, Client.MultipleObjectsReturned):
            client = None
            client_groups = None  # Disable filtering by client groups since no or multiple clients were found
        else:
            client_groups = client.groups.all()
        if kwargs.get('show_in_fleio', None) is None:
            kwargs.pop('show_in_fleio', None)
        if client and client_groups:
            flavors = flavors.filter(models.Q(show_to_groups__in=client_groups) | models.Q(show_to_groups__isnull=True))
        elif client:
            flavors = flavors.filter(show_to_groups__isnull=True)
        return flavors.filter(**kwargs)

    def get_for_client(self, client):
        """
        Get all flavors available for a client
        This function also filters by client groups, if the client is a member of one or more groups.
        """
        flavors = self.filter(is_public=True)
        client_groups = client.groups.all() if client else None
        if client and client_groups:
            flavors = flavors.filter(
                models.Q(show_to_groups__in=client_groups) | models.Q(show_to_groups__isnull=True)
            )
        elif client:
            flavors = flavors.filter(show_to_groups__isnull=True)
        return flavors


@python_2_unicode_compatible
class OpenstackInstanceFlavor(models.Model):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1024, blank=True)
    memory_mb = models.IntegerField()
    vcpus = models.IntegerField(default=1)
    swap = models.IntegerField(default=0)
    vcpu_weight = models.IntegerField(blank=True, null=True)
    rxtx_factor = models.FloatField(blank=True, null=True)
    root_gb = models.IntegerField(blank=True, null=True)
    ephemeral_gb = models.IntegerField(blank=True, null=True)
    disabled = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    region = models.ForeignKey('openstack.OpenstackRegion', related_name='flavors', db_constraint=False,
                               null=True, blank=True, on_delete=models.DO_NOTHING)
    show_in_fleio = models.BooleanField(default=True)
    out_of_stock = models.BooleanField(default=False)
    show_to_groups = models.ManyToManyField(ClientGroup, blank=True)
    flavor_group = models.ForeignKey(FlavorGroup, null=True, blank=True, on_delete=models.PROTECT)
    properties = models.CharField(max_length=10240, null=True, blank=True)

    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='flavors',
        default=None,
        null=True,
        blank=True,
    )

    used_by_resellers = models.ManyToManyField(
        'reseller.ResellerResources',
        related_name='visible_staff_flavors'
    )

    objects = FlavorManager()

    class Meta:
        verbose_name_plural = 'Flavors'
        unique_together = ('id', 'name', 'region')
        ordering = ['name']

    def __str__(self):
        return "{0} - {1}".format(self.name, self.region.id)

    @property
    def memory_gb(self):
        with decimal.localcontext() as ctx:
            ctx.prec = 2
            memory_gb = decimal.Decimal(self.memory_mb) / 1024
        return memory_gb
