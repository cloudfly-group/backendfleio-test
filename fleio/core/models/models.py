import datetime
from decimal import Decimal
import pycountry

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.utils.functional import cached_property
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from fleio.core.utils import RandomId
from fleio.conf.models import Configuration
from fleio.utils.model import dict_to_choices

# FIXME(tomo): Dependency on fleio.billing for core ?
from fleio.billing.settings import BillingSettings as ConfBillingSettings


def get_default_currency():
    try:
        return Currency.objects.get(is_default=True)
    except (Currency.MultipleObjectsReturned, Currency.DoesNotExist):
        return None


class PermissionNames(object):
    api_users_create = 'apiusers.create'
    api_users_update = 'apiusers.update'
    api_users_destroy = 'apiusers.destroy'
    clients_destroy = 'clients.destroy'
    clusters_create = 'clusters.create'
    clusters_update = 'clusters.update'
    clusters_destroy = 'clusters.destroy'
    clusters_resize = 'clusters.resize'
    clusters_get_certificate = 'clusters.get_certificate'
    cluster_templates_create = 'clustertemplates.create'
    cluster_templates_update = 'clustertemplates.update'
    cluster_templates_destroy = 'clustertemplates.destroy'
    zones_create = 'dns.create'
    zones_update = 'dns.update'
    zones_destroy = 'dns.destroy'
    zones_synchronize_records = 'dns.synchronize_records'
    zones_create_or_update_ptr = 'dns.create_or_update_ptr'
    instance_create = 'instances.create'
    instance_abort_migrate = 'instances.abort-migrate'
    instance_attach_volume = 'instances.attach-volume'
    instance_change_password = 'instances.change-password'
    instance_confirm_resize = 'instances.confirm-resize'
    instance_create_snapshot = 'instances.create_snapshot'
    instance_detach_volume = 'instances.detach_volume'
    instance_destroy = 'instances.destroy'
    instance_lock = 'instances.lock'
    instance_migrate = 'instances.migrate'
    instance_move = 'instances.move'
    instance_reboot = 'instances.reboot'
    instance_rebuild = 'instances.rebuild'
    instance_rename = 'instances.rename'
    instance_rescue = 'instances.rescue'
    instance_boot_from_iso = 'instances.boot_from_iso'
    instance_reset_state = 'instances.reset-state'
    instance_resize = 'instances.resize'
    instance_resume = 'instances.resume'
    instance_revert_resize = 'instances.revert-resize'
    instance_start = 'instances.start'
    instance_stop = 'instances.stop'
    instance_suspend = 'instances.suspend'
    instance_unlock = 'instances.unlock'
    instance_unrescue = 'instances.unrescue'
    instance_dissociate_security_group = 'instances.dissociate_security_group'
    instance_associate_security_group = 'instances.associate_security_group'
    instance_create_backup = 'instances.create_backup'
    instance_add_floating_ip = 'instances.add_floating_ip'
    instance_remove_floating_ip = 'instances.remove_floating_ip'
    volume_create = 'volumes.create'
    volume_destroy = 'volumes.destroy'
    volume_extend = 'volumes.extend'
    volume_rename = 'volumes.rename'
    volume_change_bootable = 'volumes.change_bootable_status'
    volume_revert_to_snapshot = 'volumes.revert_to_snapshot'
    volume_backup_create = 'volumebackups.create'
    volume_backup_update = 'volumebackups.update'
    volume_backup_restore = 'volumebackups.restore'
    volume_backup_destroy = 'volumebackups.destroy'
    volume_snapshot_create = 'volumesnapshots.create'
    volume_snapshot_update = 'volumesnapshots.update'
    volume_snapshot_destroy = 'volumesnapshots.destroy'
    volume_snapshot_reset_state = 'volumesnapshots.reset-state'
    image_create = 'images.create'
    image_destroy = 'images.destroy'
    image_download = 'images.download'
    image_update = 'images.update'
    image_deactivate = 'images.deactivate'
    image_reactivate = 'images.reactivate'
    flavor_create = 'flavors.create'
    flavor_destroy = 'flavors.destroy'
    flavor_update = 'flavors.update'
    project_create = 'projects.create'
    project_delete = 'projects.delete_project'
    project_update = 'projects.update'
    router_create = 'routers.create'
    router_update = 'routers.update'
    router_destroy = 'routers.destroy'
    router_add_interface = 'routers.add_interface'
    router_remove_interface = 'routers.remove_interface'
    service_destroy = 'services.destroy'
    network_create = 'networks.create'
    network_destroy = 'networks.destroy'
    network_auto_create_network = 'networks.auto_create_network'
    network_update = 'networks.update'
    network_save_auto_create_network_options = 'networks.save_auto_create_network_options'
    floatingips_create = 'floatingips.create'
    floatingips_destroy = 'floatingips.destroy'
    securitygroup_create = 'securitygroups.create'
    securitygroup_update = 'securitygroups.update'
    securitygroup_add_rule = 'securitygroups.add_rule'
    securitygroup_delete_rule = 'securitygroups.delete_rule'
    securitygroup_destroy = 'securitygroups.destroy'
    subnetpools_create = 'subnetpools.create'
    subnetpools_update = 'subnetpools.update'
    subnetpools_destroy = 'subnetpools.destroy'
    pkm_create = 'publickeys.create'
    pkm_update = 'publickeys.update'
    pkm_destroy = 'publickeys.destroy'
    ports_create = 'ports.create'
    ports_add_ip = 'ports.add_ip'
    ports_auto_add_ip = 'ports.automatic_add_ips'
    ports_remove_ip = 'ports.remove_ip'
    ports_destroy = 'ports.destroy'
    revenue_reports_list = 'revenue_reports.list'
    revenue_reports_retrieve = 'revenue_reports.retrieve'
    revenue_reports_generate = 'revenue_reports.trigger_revenue_report_generation'
    revenue_reports_update = 'revenue_reports.update'
    revenue_reports_destroy = 'revenue_reports.destroy'

    permissions_map = {
        api_users_create: _('API Users - Create'),
        api_users_update: _('API Users - Update'),
        api_users_destroy: _('API Users - Destroy'),
        clients_destroy: _('Clients - Destroy'),
        clusters_create: _('Clusters - Create'),
        clusters_update: _('Clusters - Update'),
        clusters_destroy: _('Clusters - Destroy'),
        clusters_resize: _('Clusters - Resize'),
        clusters_get_certificate: _('Clusters - Get certificate'),
        cluster_templates_create: _('Cluster templates - Create'),
        cluster_templates_update: _('Cluster templates - Update'),
        cluster_templates_destroy: _('Cluster templates - Destroy'),
        zones_create: _('Zones - Create'),
        zones_update: _('Zones - Update'),
        zones_destroy: _('Zones - Destroy'),
        zones_synchronize_records: _('Zones - Update zone records'),
        zones_create_or_update_ptr: _('Zones - Create or update PTR'),
        instance_create: _('Instance - Create'),
        instance_abort_migrate: _('Instance - Abort migrate'),
        instance_attach_volume: _('Instance - Attach volume'),
        instance_change_password: _('Instance - Change password'),
        instance_confirm_resize: _('Instance - Confirm resize'),
        instance_create_snapshot: _('Instance - Create snapshot'),
        instance_detach_volume: _('Instance - Detach volume'),
        instance_destroy: _('Instance - Destroy'),
        instance_lock: _('Instance - Lock'),
        instance_migrate: _('Instance - Migrate'),
        instance_move: _('Instance - Move'),
        instance_reboot: _('Instance - Reboot'),
        instance_rebuild: _('Instance - Rebuild'),
        instance_rename: _('Instance - Rename'),
        instance_rescue: _('Instance - Rescue'),
        instance_boot_from_iso: _('Instance - Boot from ISO'),
        instance_reset_state: _('Instance - Reset state'),
        instance_resize: _('Instance - Resize'),
        instance_resume: _('Instance - Resume'),
        instance_revert_resize: _('Instance - Revert resize'),
        instance_start: _('Instance - Start'),
        instance_stop: _('Instance - Stop'),
        instance_suspend: _('Instance - Suspend'),
        instance_unlock: _('Instance - Unlock'),
        instance_unrescue: _('Instance - Unrescue'),
        instance_dissociate_security_group: _('Instance - Dissociate security group'),
        instance_associate_security_group: _('Instance - Associate security group'),
        instance_create_backup: _('Instance - Create backup'),
        instance_add_floating_ip: _('Instance - Associate floating IP'),
        instance_remove_floating_ip: _('Instance - Dissociate floating IP'),
        volume_create: _('Volume - Create'),
        volume_destroy: _('Volume - Destroy'),
        volume_extend: _('Volume - Extend'),
        volume_rename: _('Volume - Rename'),
        volume_change_bootable: _('Volume - Change bootable status'),
        volume_revert_to_snapshot: _('Volume - Revert to snapshot'),
        volume_backup_update: _('Volume backup - Update'),
        volume_backup_create: _('Volume backup - Create'),
        volume_backup_restore: _('Volume backup - Restore'),
        volume_backup_destroy: _('Volume backup - Destroy'),
        volume_snapshot_create: _('Volume snapshot - Create'),
        volume_snapshot_update: _('Volume snapshot - Update'),
        volume_snapshot_destroy: _('Volume snapshot - Destroy'),
        volume_snapshot_reset_state: _('Volume snapshot - Reset state'),
        image_create: _('Image - Create'),
        image_destroy: _('Image - Destroy'),
        image_download: _('Image - Download'),
        image_update: _('Image - Update'),
        image_deactivate: _('Image - Deactivate'),
        image_reactivate: _('Image - Reactivate'),
        flavor_create: _('Flavor - Create'),
        flavor_destroy: _('Flavor - Destroy'),
        flavor_update: _('Flavor - Update'),
        project_create: _('Project - Create'),
        project_delete: _('Project - Delete'),
        project_update: _('Project - Update'),
        router_create: _('Router - Create'),
        router_update: _('Router - Update'),
        router_destroy: _('Router - Destroy'),
        router_add_interface: _('Router - Add interface'),
        router_remove_interface: _('Router - Remove interface'),
        service_destroy: _('Service - Delete a service'),
        network_create: _('Network - Create'),
        network_destroy: _('Network - Destroy'),
        network_auto_create_network: _('Network - Auto create network'),
        network_update: _('Network - Update'),
        network_save_auto_create_network_options: _('Network - Change auto create options'),
        floatingips_create: _('Floating IPs - Create'),
        floatingips_destroy: _('Floating IPs - Destroy'),
        securitygroup_create: _('Security group - Create'),
        securitygroup_update: _('Security group - Update'),
        securitygroup_add_rule: _('Security group - Add rule'),
        securitygroup_delete_rule: _('Security group - Delete rule'),
        securitygroup_destroy: _('Security group - Delete security group'),
        subnetpools_create: _('Subnet pools - Create'),
        subnetpools_update: _('Subnet pools - Update'),
        subnetpools_destroy: _('Subnet pools - Destroy'),
        pkm_create: _('SSH keys - Create'),
        pkm_update: _('SSH keys - Update'),
        pkm_destroy: _('SSH keys - Destroy'),
        ports_create: _('Ports - Create'),
        ports_add_ip: _('Ports - Add IP'),
        ports_auto_add_ip: _('Ports - Automatically add IP'),
        ports_remove_ip: _('Ports - Remove IP'),
        ports_destroy: _('Ports - Destroy'),
        revenue_reports_list: _('Revenue reports - See the revenue reports list'),
        revenue_reports_retrieve: _('Revenue reports - See a revenue report details'),
        revenue_reports_generate: _('Revenue reports - Generate revenue report'),
        revenue_reports_update: _('Revenue reports - Update a revenue report'),
        revenue_reports_destroy: _('Revenue reports - Delete a revenue report'),
    }

    permissions_description_map = {
        api_users_create: _('Allows users to create API users'),
        api_users_update: _('Allows users to update API users'),
        api_users_destroy: _('Allows users to delete API users'),
        clients_destroy: _('Allows users to delete a client and his resources.'),
        clusters_create: _('Allows users to create clusters'),
        clusters_update: _('Allows users to update clusters'),
        clusters_destroy: _('Allows users to delete clusters'),
        clusters_resize: _('Allows users to resize a cluster'),
        clusters_get_certificate: _('Allows users to get a cluster certificate'),
        cluster_templates_create: _('Allows users to create cluster templates'),
        cluster_templates_update: _('Allows users to update cluster templates'),
        cluster_templates_destroy: _('Allows users to delete cluster templates'),
        zones_create: _('Allows users to create zones'),
        zones_update: _('Allows users to update zones'),
        zones_destroy: _('Allows users to delete a zone'),
        zones_synchronize_records: _('Allows users to update zone records'),
        zones_create_or_update_ptr: _('Allows users to create or update PTR'),
        instance_create: _('Allows users to create an instance'),
        instance_abort_migrate: _('Allows users to migrate an instance'),
        instance_attach_volume: _('Allows users to attach a volume to an instance'),
        instance_change_password: _('Allows users to change an instance password'),
        instance_confirm_resize: _('Allows users to confirm resize of an instance'),
        instance_create_snapshot: _('Allows users to create a snapshot of an instance'),
        instance_detach_volume: _('Allows users to detach a volume from an instance'),
        instance_destroy: _('Allows users to delete an instance'),
        instance_lock: _('Allows users to lock an instance'),
        instance_migrate: _('Allows users to migrate an instance'),
        instance_move: _('Allows staff users to move an instance'),
        instance_reboot: _('Allows users to reboot an instance'),
        instance_rebuild: _('Allows users to rebuild an instance'),
        instance_rename: _('Allows users to rename an instance'),
        instance_rescue: _('Allows users to rescue an instance'),
        instance_reset_state: _('Allows users to reset state of an instance'),
        instance_resize: _('Allows users to resize an instance'),
        instance_resume: _('Allows users to resume an instance'),
        instance_revert_resize: _('Allows users to revert resize of an instance'),
        instance_start: _('Allows users to start an instance'),
        instance_stop: _('Allows users to stop an instance'),
        instance_suspend: _('Allows users to suspend an instance'),
        instance_unlock: _('Allows users to unlock an instance'),
        instance_unrescue: _('Allows users to unrescue an instance'),
        instance_dissociate_security_group: _('Allows users to dissociate a security group'),
        instance_associate_security_group: _('Allows users to associate a security group'),
        instance_create_backup: _('Allows users to create an instance backup'),
        instance_add_floating_ip: _('Allows users to associate a floating IP'),
        instance_remove_floating_ip: _('Allows users to dissociate a floating IP'),
        volume_create: _('Allows users to create a volume'),
        volume_destroy: _('Allows users to delete a volume'),
        volume_extend: _('Allows users to extend a volume'),
        volume_rename: _('Allows users to rename a volume'),
        volume_change_bootable: _('Allows users to change bootable status for a volume'),
        volume_revert_to_snapshot: _('Allows users to revert volume to snapshot'),
        volume_backup_update: _('Allows users to update a volume backup'),
        volume_backup_create: _('Allows users to create a volume backup'),
        volume_backup_restore: _('Allows users to restore a volume backup'),
        volume_backup_destroy: _('Allows users to delete a volume backup'),
        volume_snapshot_create: _('Allows users to create a volume snapshot'),
        volume_snapshot_update: _('Allows users to update a volume snapshot'),
        volume_snapshot_destroy: _('Allows users to delete a volume snapshot'),
        volume_snapshot_reset_state: _('Allows users to reset state of a volume snapshot'),
        image_create: _('Allows users to create an image'),
        image_destroy: _('Allows users to delete an image'),
        image_download: _('Allows users to download an image'),
        image_update: _('Allows users to update an image'),
        image_deactivate: _('Allows users to deactivate an image'),
        image_reactivate: _('Allows users to reactivate an image'),
        flavor_create: _('Allows users to create a flavor'),
        flavor_destroy: _('Allows users to delete a flavor'),
        flavor_update: _('Allows users to update a flavor'),
        project_create: _('Allows users to create a project'),
        project_delete: _('Allows users to delete an openstack project'),
        project_update: _('Allows users to update an openstack project'),
        router_create: _('Allows users to create a router'),
        router_update: _('Allows users to update a router'),
        router_destroy: _('Allows users to delete a router'),
        router_add_interface: _('Allows users to add an interface to a router'),
        router_remove_interface: _('Allows users to remove an interface from a router'),
        service_destroy: _('Allows a user to delete a service and its related resources'),
        network_create: _('Allows users to create a network'),
        network_destroy: _('Allows users to delete a network'),
        network_auto_create_network: _('Allows users to auto create a network'),
        network_update: _('Allows users to update a network'),
        network_save_auto_create_network_options: _('Allows staff users to change auto create network options'),
        floatingips_create: _('Allows users to create floating IPs'),
        floatingips_destroy: _('Allows users to delete floating IPs'),
        securitygroup_create: _('Allows users to create a security group'),
        securitygroup_update: _('Allows users to update a security group'),
        securitygroup_add_rule: _('Allows users to add rules to a security group'),
        securitygroup_delete_rule: _('Allows users to delete rules from a security group'),
        securitygroup_destroy: _('Allows users to delete a security group'),
        subnetpools_create: _('Allows users to create a subnet pool'),
        subnetpools_update: _('Allows users to update a subnet pool'),
        subnetpools_destroy: _('Allows users to delete a subnet pool'),
        pkm_create: _('Allows users to create a SSH key'),
        pkm_update: _('Allows users to update a SSH key'),
        pkm_destroy: _('Allows users to delete a SSH key'),
        ports_create: _('Allows users to create a port'),
        ports_add_ip: _('Allows users to add IPs'),
        ports_auto_add_ip: _('Allows users to automatically add IPs'),
        ports_remove_ip: _('Allows users to remove an ip'),
        ports_destroy: _('Allows users to delete a port'),
        revenue_reports_list: _('Allows users to see the list of revenue reports'),
        revenue_reports_retrieve: _('Allows users to see the details of a revenue report'),
        revenue_reports_generate: _('Allows users to generate revenue reports'),
        revenue_reports_update: _('Allows users to update revenue reports'),
        revenue_reports_destroy: _('Allows users to delete revenue reports'),
    }

    @classmethod
    def get_choices(cls):
        return dict_to_choices(cls.permissions_map)


class PermissionSet(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    implicitly_granted = models.BooleanField()

    class Meta:
        app_label = 'core'

    def __str__(self):
        return self.name

    def permission_granted(self, permission_name: str) -> bool:
        permission = self.permissions.filter(name=permission_name).first()

        if permission:
            return permission.granted
        else:
            return self.implicitly_granted


class Permission(models.Model):
    permission_set = models.ForeignKey(PermissionSet, related_name='permissions', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    granted = models.BooleanField()

    class Meta:
        unique_together = ('permission_set', 'name')
        app_label = 'core'


class UserGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=1024, null=True, blank=True)
    permissions = models.OneToOneField(PermissionSet, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    is_default = models.BooleanField(default=False)
    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='user_groups',
        default=None,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.is_default:
            UserGroup.objects.filter(is_default=True).update(is_default=False)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = 'core'

    def __str__(self):
        return self.name


class AppUser(AbstractUser, PermissionsMixin):
    id = models.BigIntegerField(unique=True, default=RandomId('core.AppUser'), primary_key=True)
    email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, blank=True)
    external_billing_id = models.CharField(blank=True, null=True, max_length=38, unique=True)
    is_superuser = models.BooleanField(default=False,
                                       help_text=('Designates that this user has all '
                                                  'permissions without explicitly assigning them.'),
                                       verbose_name='superuser status')
    permissions = models.OneToOneField(PermissionSet, on_delete=models.SET_NULL, null=True, blank=True)
    user_groups = models.ManyToManyField(UserGroup, related_name='users', blank=True)
    mobile_phone_number = models.CharField(max_length=64, null=True, blank=True)
    is_reseller = models.BooleanField(
        _('reseller status'),
        default=False,
        help_text=_('Designates whether the user is a reseller.'),
    )
    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='users',
        default=None,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = 'core'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return None

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def can_impersonate(self):
        return self.is_staff or self.is_reseller

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser or self.is_reseller

    @property
    def clients_suspended(self) -> bool:
        return self.clients.filter(status=ClientStatus.suspended).count() > 0


class CurrencyManager(models.Manager):
    def get_default_or_first(self):
        return self.filter(is_default=True).first() or self.first()


class Currency(models.Model):
    code = models.CharField(max_length=3,
                            primary_key=True,
                            choices=[(i.alpha_3, i.alpha_3) for i in pycountry.currencies])
    rate = models.DecimalField(default=1, max_digits=12, decimal_places=6)
    is_default = models.BooleanField(default=False)

    objects = CurrencyManager()

    class Meta:
        verbose_name_plural = 'currencies'
        app_label = 'core'

    def to_dict(self):
        return dict(code=self.code, rate=self.rate, is_default=self.is_default)

    def save(self, *args, **kwargs):
        if self.is_default:
            # NOTE(tomo): Remove any other defaults
            Currency.objects.filter(is_default=True).exclude(code=self.code).update(is_default=False)
        return super(Currency, self).save(*args, **kwargs)

    def __str__(self):
        return self.code


class ClientGroup(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)
    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='client_groups',
        default=None,
        null=True,
        blank=True,
    )

    objects = models.Manager

    def save(self, *args, **kwargs):
        if self.is_default:
            ClientGroup.objects.filter(is_default=True).update(is_default=False)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClientStatus(object):
    active = 'active'
    inactive = 'inactive'
    suspended = 'suspended'
    closed = 'closed'
    deleting = 'deleting'

    choices = [(active, _('Active')),
               (inactive, _('Inactive')),
               (suspended, _('Suspended')),
               (closed, _('Closed')),
               (deleting, _('Deleting'))]


class ClientSuspendReason(object):
    user = 'user'
    auto = 'auto'

    choices = [(user, _('user action')),
               (auto, _('automatic action'))]


class ClientQueryset(models.QuerySet):
    def active(self):
        return self.filter(status=ClientStatus.active)


class Client(models.Model):
    id = models.BigIntegerField(unique=True, default=RandomId('core.Client'), primary_key=True)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    company = models.CharField(max_length=127, blank=True, null=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=127)
    country = models.CharField(max_length=2, db_index=True, choices=[(country.alpha_2, country.name)
                                                                     for country in pycountry.countries])
    state = models.CharField(max_length=127, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=64)
    fax = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=127)
    date_created = models.DateTimeField(db_index=True, auto_now_add=True)
    currency = models.ForeignKey(Currency, default=get_default_currency, on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clients', through='UserToClient')
    external_billing_id = models.CharField(null=True, blank=True, unique=True, max_length=38)
    groups = models.ManyToManyField(ClientGroup, related_name='clients', blank=True)
    vat_id = models.CharField(null=True, max_length=32, blank=True)
    tax_exempt = models.BooleanField(default=False)
    configuration = models.ForeignKey('conf.Configuration', null=True, blank=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=ClientStatus.choices, db_index=True, default='active')
    suspend_reason = models.CharField(max_length=16, choices=ClientSuspendReason.choices,
                                      db_index=True, default='active')
    outofcredit_datetime = models.DateTimeField(db_index=True, null=True, blank=True)
    uptodate_credit = models.DecimalField(null=True, decimal_places=2, max_digits=14)
    has_billing_agreement = models.BooleanField(default=False)

    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='clients',
        default=None,
        null=True,
        blank=True,
    )

    objects = ClientQueryset.as_manager()

    class Meta:
        app_label = 'core'
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if self.configuration is None or self.configuration.reseller_resources != self.reseller_resources:
            # Set the default configuration for new clients
            try:
                self.configuration = Configuration.objects.default(reseller_resources=self.reseller_resources)
            except Configuration.DoesNotExist:
                pass
        return super(Client, self).save(*args, **kwargs)

    # TODO: this should not be created here
    @property
    def billing_settings(self) -> ConfBillingSettings:
        if self.configuration:
            return ConfBillingSettings(configuration_id=self.configuration_id)
        else:
            try:
                default_config = Configuration.objects.default(reseller_resources=self.reseller_resources)
            except Configuration.DoesNotExist:
                return ConfBillingSettings()
            else:
                return ConfBillingSettings(configuration_id=default_config.id)

    @cached_property
    def active_configuration(self):
        """Gets active configuration for client or None if not found."""
        if self.configuration is not None:
            return self.configuration
        else:
            return Configuration.objects.default(reseller_resources=self.reseller_resources)

    # TODO: this property should be removed
    # Instead of projects we should check and display services
    # The client class should not be aware of open stack projects
    @property
    def first_project(self):
        # FIXME(tomo): use a better way to disable OpenStack in Fleio
        if 'fleio.openstack' not in settings.INSTALLED_APPS:
            return None
        openstack_service = self.services.filter(
            openstack_project__isnull=False
        ).exclude(status='terminated').first()
        if openstack_service is not None:
            return openstack_service.openstack_project
        else:
            return None

    @cached_property
    def country_name(self):
        return pycountry.countries.get(alpha_2=self.country).name

    @cached_property
    def long_name(self):
        if self.company:
            return '{0} ({1} {2})'.format(self.company, self.first_name, self.last_name)
        else:
            return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.name

    @cached_property
    def name(self):
        if not self.first_name:
            return '{}'.format(self.company)
        else:
            return '{} {}'.format(self.first_name, self.last_name)

    def add_credit(self, amount, currency):
        """Add amount to client credit account in specified currency
        :type amount: decimal.Decimal
        :type currency: Currency
        """
        credit_account = self.credits.deposit(client=self, currency=currency, amount=amount)
        return credit_account.amount

    def withdraw_credit(self, amount, currency):
        """Withdraw amount from client credit account in specified currency
        :type amount: decimal.Decimal
        :type currency: Currency
        """
        credit_account = self.credits.withdraw(client=self, currency=currency, amount=amount)
        return credit_account.amount

    def get_remaining_credit(self, amount, currency_code):
        try:
            credit = self.credits.get(client=self, currency__code=currency_code)
        except ObjectDoesNotExist:
            return -amount
        else:
            return credit.amount - amount

    def set_outofcredit(self, outofcredit_datetime: datetime.datetime = True):
        if self.is_outofcredit:
            return

        self.outofcredit_datetime = outofcredit_datetime
        self.save(update_fields=['outofcredit_datetime'])

    def clear_outofcredit(self):
        if not self.is_outofcredit:
            return

        self.outofcredit_datetime = None
        self.save(update_fields=['outofcredit_datetime'])

    @property
    def is_outofcredit(self) -> bool:
        return not not self.outofcredit_datetime

    def get_hours_since_outofcredit(self, reference_datetime: datetime.datetime) -> Decimal:
        if self.is_outofcredit:
            if reference_datetime > self.outofcredit_datetime:
                return Decimal((reference_datetime - self.outofcredit_datetime).total_seconds() / 3600)

        return Decimal(0)

    @property
    def has_uptodate_credit(self) -> bool:
        return self.uptodate_credit is not None

    def get_uptodate_credit(self) -> Decimal:
        if self.uptodate_credit is None:
            return Decimal('0.00')
        else:
            return self.uptodate_credit

    def set_uptodate_credit(self, uptodate_credit: Decimal):
        self.uptodate_credit = uptodate_credit
        self.save(update_fields=['uptodate_credit'])

    def set_active(self):
        if self.status != ClientStatus.active:
            self.status = ClientStatus.active
            self.save(update_fields=['status'])


class UserToClient(models.Model):
    """
    Map user accounts to Client objects and store permissions

    Also stores (email) communications and notifications settings.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # When is_client_admin=True user can modify client settings, can add other
    # users and all other rights are considered True
    is_client_admin = models.BooleanField(default=False)
    permissions = models.CharField(validators=[validate_comma_separated_integer_list], max_length=255)

    class Meta:
        unique_together = ('user', 'client')
        app_label = 'core'

    def __str__(self):
        return "{0} / {1}".format(self.user, self.client)

    def has_perm(self, perm):
        """Checks if self.user has the perm permission for self.client."""
        return self.is_client_admin or (str(perm) in self.permissions.split(','))

    def add_perm(self, perm):
        pass

    def remove_perm(self, perm):
        pass


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_id = models.CharField(max_length=8, blank=True, null=True, unique=True)

    class Meta:
        app_label = 'core'


class PluginManager(models.Manager):
    def enabled(self):
        return self.filter(enabled=True)

    def loaded(self):
        return self.filter(app_loaded=True)


class Plugin(models.Model):
    display_name = models.CharField(max_length=100, null=False, blank=False)
    app_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    app_label = models.CharField(max_length=100, null=False, blank=False, unique=True)
    feature_name = models.CharField(max_length=100, null=True, blank=False, unique=False)
    staff_feature_name = models.CharField(max_length=100, null=True, blank=False, unique=False)
    app_loaded = models.BooleanField()
    enabled = models.BooleanField(default=True)

    objects = PluginManager()

    def __str__(self):
        return '{}({})'.format(self.display_name, self.app_name)

    class Meta:
        app_label = 'core'
