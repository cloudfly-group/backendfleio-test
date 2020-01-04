import logging

from django.db import models
from django.db import transaction
from django.db.utils import IntegrityError
from django.template import Context
from django.template import Template
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.billing.models import Product
from fleio.billing.models import Service
from fleio.billing.settings import ServiceStatus
from fleio.core.utils import RandomId
from fleio.openstack import settings
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.api.session import get_session
from fleio.openstack.utils import OSAuthCache
from fleio.osbilling.service_helper import ServiceHelper

LOG = logging.getLogger(__name__)


class ProjectManager(models.Manager):
    def create_project(self, client, openstack_product=None, openstack_product_cycle=None, **kwargs):
        """
        Create the project with the OpenStack Keystone API, add `admin` (plugin_settings.USERNAME)
        user rights (plugin_settings.DEFAULT_ROLE) to it and return the corresponding Fleio database object.
        """
        extra_fields = kwargs.copy()
        admin_api = IdentityAdminApi()

        service_external_id = extra_fields.pop('service_external_id', None)
        if 'project_id' not in extra_fields:
            project_context = {'client': client}
            try:
                project_name = Template(settings.plugin_settings.default_project_name).render(Context(project_context))
                desc_tpl = settings.plugin_settings.default_project_description
                project_description = Template(desc_tpl).render(Context(project_context))
            except Exception as e:
                LOG.exception(e)
                project_name = '{} - {}'.format(client.name, client.id)
                project_description = 'Fleio created for {}'.format(client.name)

            project = admin_api.create_project(project_name,
                                               settings.plugin_settings.PROJECT_DOMAIN_ID,
                                               project_description)
            admin_api.grant_user_role(project.id,
                                      settings.plugin_settings.USERNAME,
                                      settings.plugin_settings.DEFAULT_ROLE)

            extra_fields['project_id'] = project.id
            extra_fields['name'] = project_name
            extra_fields['description'] = project_description
        else:
            admin_api.grant_user_role(extra_fields['project_id'],
                                      settings.plugin_settings.USERNAME,
                                      settings.plugin_settings.DEFAULT_ROLE)

        if openstack_product is None:
            # no openstack product provided, get product from client configuration
            client_configuration = client.billing_settings

            try:
                openstack_product = Product.objects.get(id=client_configuration.auto_order_service)
            except Product.DoesNotExist:
                openstack_product = Product.objects.filter(product_type='openstack').first()
            if openstack_product:
                cycle_id = client_configuration.auto_order_service_cycle
                openstack_product_cycle = openstack_product.cycles.filter(id=cycle_id).first()
            else:
                openstack_product_cycle = None

        try:
            with transaction.atomic():
                # create service
                service = self.create_service(client, openstack_product, openstack_product_cycle, service_external_id)

                # create project
                db_project = self.create(service=service, **extra_fields)
        except IntegrityError:
            # TODO: we are getting integrity errors because updated manages to create project first
            # attempt to update existing project
            db_project = self.filter(project_id=extra_fields['project_id']).first()
            if db_project is not None:
                with transaction.atomic():
                    # create service for project
                    service = self.create_service(
                        client,
                        openstack_product,
                        openstack_product_cycle,
                        service_external_id
                    )

                    db_project.service = service
                    db_project.save(update_fields=['service'])
            else:
                LOG.error('Failed to create or update project')

        return db_project

    @staticmethod
    def create_service(client, openstack_product, openstack_product_cycle, service_external_id):
        # create service for project
        service = Service()
        service.display_name = 'OpenStack Project'
        service.client = client
        service.product = openstack_product
        service.cycle = openstack_product_cycle
        service.created_at = utcnow()
        service.activated_at = utcnow()
        service.status = ServiceStatus.active
        service.external_billing_id = service_external_id
        service.update_next_due_date(save_to_database=False)
        service.update_next_invoice_date(save_to_database=False)
        service.save()

        ServiceHelper.init_service_dynamic_usage(service)

        return service


@python_2_unicode_compatible
class Project(models.Model):
    """Relationship between a billing client and a Keystone project."""
    DISABLED_NEED_PAYMENT = 'need_payment'
    DISABLED_ADMIN_LOCKED = 'admin_locked'
    DISABLED_REASON_CHOICES = ((DISABLED_NEED_PAYMENT, DISABLED_NEED_PAYMENT),
                               (DISABLED_ADMIN_LOCKED, DISABLED_ADMIN_LOCKED),)

    id = models.BigIntegerField(unique=True, default=RandomId('openstack.Project'), primary_key=True)
    service = models.OneToOneField(Service,
                                   related_name='openstack_project',
                                   on_delete=models.SET_NULL,
                                   db_index=True,
                                   null=True)
    project_id = models.CharField(max_length=36, unique=True)
    project_domain_id = models.CharField(max_length=36, blank=True)
    deleted = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    fleio_disabled_reason = models.CharField(choices=DISABLED_REASON_CHOICES, max_length=16, null=True,
                                             blank=True, db_index=True)
    extras = JSONField(null=True, blank=True)
    sync_version = models.BigIntegerField(default=0)
    is_domain = models.BooleanField(default=False)
    name = models.CharField(default=None, null=True, max_length=255)
    description = models.CharField(default=None, null=True, max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = ProjectManager()

    class Meta:
        verbose_name_plural = 'Services to projects'
        unique_together = ('service', 'project_id')

    def __str__(self):
        try:
            if self.service:
                return "{0} {1} / {2}".format(
                    self.service.client.first_name,
                    self.service.client.last_name,
                    self.project_id)
            else:
                return '{}'.format(self.project_id)
        except Exception as e:
            LOG.exception(e)
            return _('n/a')

    def get_session(self, request_session=None):
        """
        :type request_session: dict, A request session or dict for caching
        :rtype: keystoneauth1.session.Session
        """
        cache = None
        if request_session:
            cache = OSAuthCache(request_session)
        plugin_settings = settings.plugin_settings
        scoped_session = get_session(auth_url=plugin_settings.AUTH_URL,
                                     project_id=self.project_id,
                                     project_domain_id=self.project_domain_id,
                                     admin_username=plugin_settings.USERNAME,
                                     admin_password=plugin_settings.PASSWORD,
                                     admin_domain_id=plugin_settings.USER_DOMAIN_ID,
                                     cache=cache)
        return scoped_session

    def set_disabled(self, value=True, reason=None):
        self.disabled = value
        self.fleio_disabled_reason = reason
        self.save(update_fields=['disabled', 'fleio_disabled_reason'])

    def set_extra(self, attr, value):
        if self.extras is None:
            self.extras = dict()
        self.extras[attr] = value
        self.save(update_fields=['extras'])

    def del_extra(self, attr):
        self.extras.pop(attr, None)
        self.save(update_fields=['extras'])
