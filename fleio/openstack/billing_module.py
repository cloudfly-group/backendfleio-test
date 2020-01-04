from celery.canvas import Signature
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from importlib import import_module
import logging
import sys
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from neutronclient.common import exceptions as neutron_exceptions

from django.db import transaction
from django.db.utils import IntegrityError
from django.template import Context
from django.template import Template
from django.utils.translation import ugettext_lazy as _

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service
from fleio.billing.modules.base import ModuleBase
from fleio.billing.modules.base import ServiceUsage
from fleio.billing.modules.utils import delete_service_resources_placeholder
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.usage_settings import UsageSettings
from fleio.billing.utils import cdecimal
from fleio.conf.exceptions import ConfigException
from fleio.core.exceptions import ObjectNotFound

from fleio.core.features import staff_active_features

from fleio.osbilling.models import PricingPlan, ServiceDynamicUsage
from fleio.osbilling.models import ServiceDynamicUsageHistory
from fleio.osbilling.models import ClientBillingStates
from fleio.osbilling.models import ResourceUsageLog
from fleio.osbilling.notifications import get_estimated_usage
from fleio.osbilling.serializers import ServiceDynamicUsageSerializer
from fleio.osbilling.service_helper import ServiceHelper

from fleio.pkm.models import PublicKey

from fleio.openstack.osapi import OSApi
from . import tasks
from .api.identity import IdentityAdminApi
from .instances.instance_status import InstanceStatus
from .models import Image, Instance, Network, OpenstackProductSettings, Port, Project, Router, Volume
from .settings import plugin_settings

LOG = logging.getLogger(__name__)

SUMMARY_OBJECTS_TO_LOAD = 3
COLLECTOR_MODULE_NAME = 'fleio.osbilling.bin.collectorlib'
COLLECT_FUNCTION_NAME = 'gather_billing_usage_for_service'


# TODO: this class should be moved to osbilling
class OpenstackModule(ModuleBase):
    module_name = "Openstack Module"

    def initialize(self, service: Service) -> bool:
        """Initializes a new service object.
        This should be the first function called on a service.

        Keyword arguments:
            service -- the service to initialize
        Returns:
            True if service was initialized successfully
        """
        LOG.debug('{} initialize called for service {}:{}'.format(self.module_name, service.id, service))
        return True

    def create(self, service: Service) -> bool:
        LOG.debug('Openstack module create called for service {0}:{1}'.format(service.id, service))

        client = service.client

        try:
            # if service was terminated and an openstack project remained in the db to keep revenue data,
            # completely remove it
            if service.openstack_project:
                service.openstack_project.delete()
        except Exception as e:
            del e  # unused

        project_context = {'client': client}

        # TODO: maybe this should be moved to OpenstackProject
        try:
            project_name = Template(plugin_settings.default_project_name).render(Context(project_context))
        except Exception as e:
            LOG.exception(e)
            project_name = '{} - {}'.format(client.name, client.id)
        project_description = 'Fleio created for {}'.format(client.name)
        try:
            admin_api = IdentityAdminApi()
        except ConfigException:
            LOG.error('Cannot perform action because openstack settings are missing/incorrect')
            return False
        project = admin_api.create_project(project_name,
                                           plugin_settings.PROJECT_DOMAIN_ID,
                                           project_description)
        admin_api.grant_user_role(project.id,
                                  plugin_settings.USERNAME,
                                  plugin_settings.DEFAULT_ROLE)

        try:
            with transaction.atomic():
                Project.objects.create(service=service, project_id=project.id)
        except IntegrityError:
            # project may be created by updated, fetch and update
            db_project = Project.objects.get(project_id=project.id)
            db_project.service = service
            db_project.save(update_fields=['service'])

        product_settings = OpenstackProductSettings.objects.filter(product=service.product).first()
        if product_settings:
            if product_settings.run_get_me_a_network_on_auto_setup:
                # run get me a network for each defined region
                os_api = OSApi.from_project_id(project_id=project.id, auth_cache=None)
                if product_settings.network_auto_allocated_topology_regions:
                    for region in product_settings.network_auto_allocated_topology_regions.all():
                        try:
                            os_api.networks.auto_create_network(
                                project_id=project.id,
                                region=region.id,
                            )
                        except neutron_exceptions.NeutronException as e:
                            LOG.error(
                                'Could not auto allocate network topology in region {}: {}'.format(
                                    region.id, str(e)
                                )
                            )

        ServiceHelper.init_service_dynamic_usage(service)

        return True

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None, ) -> bool:
        LOG.debug('Openstack module suspend called, starting suspend task ...')

        if not hasattr(service, 'openstack_project'):
            LOG.error('Suspend called with a service with no openstack project associated, aborting.')
            return False

        # TODO: we cannot pass reason forward since project expects very specific values - we need to reorganize those
        # currently we have different suspend reason or type constants in several places
        tasks.suspend_project.delay(service.openstack_project.project_id)
        return True

    def resume(self, service: Service) -> bool:
        LOG.debug('Openstack module resume called, starting resume task ...')

        if not hasattr(service, 'openstack_project'):
            LOG.error('Resume called with a service with no openstack project associated, aborting.')
            return False

        tasks.resume_project.delay(service.openstack_project.project_id)
        return True

    def renew(self, service: Service) -> bool:
        LOG.debug('Openstack module renew called for service {0}:{1}'.format(service.id, service))
        # TODO: implement
        return True

    def change_product(self, service: Service) -> bool:
        LOG.debug('Openstack module change product called for service {0}:{1}'.format(service.id, service))
        # TODO: implement
        return True

    def change_cycle(self, service: Service) -> bool:
        LOG.debug('Openstack module change cycle called for service {0}:{1}'.format(service.id, service))
        # TODO: implement
        return True

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        LOG.debug('Openstack module delete called, starting delete task ...')
        assert type(service) is Service

        if not hasattr(service, 'openstack_project'):
            LOG.debug(
                'Delete called with a service with no openstack project associated, returning placeholder task.'
            )
            return delete_service_resources_placeholder.si()

        delete_task = tasks.delete_client_project_resources.si(
            project_id=service.openstack_project.project_id, user_id=user_id
        )
        return delete_task

    def filter_service_usage_history(self, billing_history_query, service):
        if self.reseller_usage:
            billing_history_query = billing_history_query.filter(service_dynamic_usage__reseller_service=service)
        else:
            billing_history_query = billing_history_query.filter(service_dynamic_usage__service=service)

        return billing_history_query

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        LOG.debug('Openstack get unsettled usage')

        unsettled_usage = ServiceUsage(total_cost=Decimal(0))
        billing_history_query = ServiceDynamicUsageHistory.objects.filter(
            state=ClientBillingStates.unsettled,
            end_date__lte=end_datetime,
        )
        billing_history_query = self.filter_service_usage_history(billing_history_query, service)

        for billing_history in billing_history_query.all():  # type: ServiceDynamicUsageHistory
            unsettled_usage.total_cost += billing_history.price
            billing_history.state = ClientBillingStates.invoiced
            billing_history.save()

        return unsettled_usage

    def get_unpaid_usage(self, service: Service) -> ServiceUsage:
        LOG.debug('Openstack get unsettled usage called for service {0}:{1}'.format(service.id, service))

        unpaid_usage = ServiceUsage(total_cost=Decimal(0))

        unpaid_billing_history = ServiceDynamicUsageHistory.objects.exclude(
            state=ClientBillingStates.settled
        )
        unpaid_billing_history = self.filter_service_usage_history(unpaid_billing_history, service)

        for billing_history in unpaid_billing_history.all():  # type: ServiceDynamicUsageHistory
            unpaid_usage.total_cost += billing_history.price

        try:
            if self.reseller_usage:
                if service.reseller_service_dynamic_usage:
                    unpaid_usage.total_cost += service.reseller_service_dynamic_usage.price
            else:
                if service.service_dynamic_usage:
                    unpaid_usage.total_cost += service.service_dynamic_usage.price
        except Exception as e:
            del e  # unused
            return unpaid_usage

        return unpaid_usage

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        LOG.debug('Openstack get dynamic price per second called for service {0}:{1}'.format(service.id, service))
        return get_estimated_usage(service, usage_settings=usage_settings)

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        LOG.debug('Openstack module collect usage called for service {0}:{1}'.format(service.id, service))
        try:
            import_module(COLLECTOR_MODULE_NAME)
            collect_usage_function = getattr(
                sys.modules[COLLECTOR_MODULE_NAME],
                COLLECT_FUNCTION_NAME
            )
            return collect_usage_function(service, usage_settings)
        except ConfigException:
            LOG.error('Could not collect usage because OpenStack settings are missing or incorrect')
            return False
        except Exception as e:
            LOG.exception('Exception {} when attempting to collect usage'.format(e))
            return False

    def reset_usage(self, service: Service) -> bool:
        LOG.debug('Openstack reset usage called for service {}:{}'.format(service.id, service))
        with transaction.atomic():
            service.service_dynamic_usage.billing_cycle_history.all().delete()
            service.service_dynamic_usage.price = Decimal('0.00')
            service.service_dynamic_usage.save()

            if hasattr(service, 'reseller_service_dynamic_usage'):
                service.reseller_service_dynamic_usage.billing_cycle_history.all().delete()
                service.reseller_service_dynamic_usage.price = Decimal('0.00')
                service.reseller_service_dynamic_usage.save()

            if hasattr(service, 'openstack_project'):
                ResourceUsageLog.objects.filter(
                    project_id=service.openstack_project.project_id
                ).delete()
            else:
                LOG.info('Reset usage called for service with no project, cannot clear resource usage log')

        return True

    def settle_usage(self, service: Service, end_datetime: datetime) -> bool:
        LOG.debug('Openstack settle usage called for service {0}:{1}'.format(service.id, service))

        # TODO: since no invoice reference is stored when settle usage is called all invoiced billing history
        # records will be set to settled and this may potentially settle items belonging to other invoices
        service_history_query = ServiceDynamicUsageHistory.objects.filter(
            state=ClientBillingStates.invoiced,
            end_date__lte=end_datetime.date()
        )
        service_history_query = self.filter_service_usage_history(service_history_query, service)
        service_history_query.update(state=ClientBillingStates.settled)

        return True

    def get_usage_summary(self, service: Service):
        LOG.debug('Openstack module get usage summary called for service {0}:{1}'.format(service.id, service))
        client = service.client
        project = service.openstack_project
        summary = OrderedDict()

        if staff_active_features.is_enabled('openstack.instances'):
            instance_count = Instance.objects.filter(project=project).exclude(
                status=InstanceStatus.DELETED).exclude(terminated_at__isnull=False).count()
            instances = Instance.objects.filter(project=project).exclude(
                status=InstanceStatus.DELETED).exclude(terminated_at__isnull=False)[:SUMMARY_OBJECTS_TO_LOAD]
            summary['Instances'] = {'count': instance_count,
                                    'load_count': SUMMARY_OBJECTS_TO_LOAD,
                                    'objects': [{'id': instance.id, 'name': instance.name} for instance in
                                                instances],
                                    'name': _('Instances')}

        if staff_active_features.is_enabled('openstack.volumes'):
            volume_count = Volume.objects.filter(project=project).count()
            volumes = Volume.objects.filter(project=project)[:SUMMARY_OBJECTS_TO_LOAD]
            summary['Volumes'] = {'count': volume_count,
                                  'load_count': SUMMARY_OBJECTS_TO_LOAD,
                                  'objects': [{'id': volume.id, 'name': volume.name} for volume in
                                              volumes],
                                  'name': _('Volumes')}

        if staff_active_features.is_enabled('openstack.sshkeys'):
            ssh_keys_count = PublicKey.objects.filter(user=client.users.first()).count()
            ssh_keys = PublicKey.objects.filter(user=client.users.first())[:SUMMARY_OBJECTS_TO_LOAD]
            summary['SSH keys'] = {'count': ssh_keys_count,
                                   'load_count': SUMMARY_OBJECTS_TO_LOAD,
                                   'objects': [{'id': key.id, 'name': key.name} for key in ssh_keys],
                                   'name': _('SSH keys')}

        if staff_active_features.is_enabled('openstack.networks'):
            network_count = Network.objects.get_networks_for_project(project_id=project.project_id,
                                                                     shared=False).count()
            networks = Network.objects.get_networks_for_project(project_id=project.project_id,
                                                                shared=False)[:SUMMARY_OBJECTS_TO_LOAD]
            summary['Networks'] = {'count': network_count,
                                   'load_count': SUMMARY_OBJECTS_TO_LOAD,
                                   'objects': [{'id': network.id, 'name': network.name} for network in
                                               networks],
                                   'name': _('Networks')}

        if staff_active_features.is_enabled('openstack.images'):
            image_count = Image.objects.filter(project=project).exclude(status='deleted').count()
            images = Image.objects.filter(project=project).exclude(status='deleted')[:SUMMARY_OBJECTS_TO_LOAD]
            summary['Images'] = {'count': image_count,
                                 'load_count': SUMMARY_OBJECTS_TO_LOAD,
                                 'objects': [{'id': image.id, 'name': image.name} for image in images],
                                 'name': _('Images')}

        if staff_active_features.is_enabled('openstack.routers'):
            router_count = Router.objects.filter(project_id=project.project_id).count()
            routers = Router.objects.filter(project_id=project.project_id)[:SUMMARY_OBJECTS_TO_LOAD]
            summary['Routers'] = {'count': router_count,
                                  'load_count': SUMMARY_OBJECTS_TO_LOAD,
                                  'objects': [{'id': router.id, 'name': router.name} for router in
                                              routers],
                                  'name': _('Routers')}

        if staff_active_features.is_enabled('openstack.ports'):
            port_count = Port.objects.filter(project_id=project.project_id).count()
            ports = Port.objects.filter(project_id=project.project_id)[:SUMMARY_OBJECTS_TO_LOAD]
            summary['Ports'] = {'count': port_count,
                                'load_count': SUMMARY_OBJECTS_TO_LOAD,
                                'objects': [{'id': port.id, 'name': port.name or port.id,
                                             'fixed_ips': port.fixed_ips} for port in ports],
                                'name': _('Ports')}

        return summary

    def get_billing_summary(self, service: Service):
        sdu = ServiceDynamicUsage.objects.get(
            reseller_service=service
        ) if self.reseller_usage else ServiceDynamicUsage.objects.get(
            service=service
        )
        return ServiceDynamicUsageSerializer().to_representation(instance=sdu)

    def get_service_report(self, service, start_date, end_date):
        # TODO: see what to do with this for reseller
        report = {'name': 'OpenStack resources report', 'locations': {}, 'service': None, 'location_cost': {}}
        location_details = {}
        default_region = plugin_settings.DEFAULT_REGION
        client = service.client
        try:
            from fleio.osbilling.bin.collectorlib import service_usage
            from fleio.osbilling.bin.collectorlib import add_pricing
            from fleio.osbilling.bin.collectorlib import collect_project_metrics
            from fleio.osbilling.bin.collectorlib import collect_internal_usage
        except ImportError:
            return report
        usage_settings = UsageSettings(billing_settings=client.billing_settings)
        try:
            usage = service_usage(
                start_date=start_date,
                end_date=end_date,
                service_dynamic_usage=service.service_dynamic_usage,
            )
        except ObjectDoesNotExist:
            return report
        usage['metrics_details'] = collect_project_metrics(
            start_date,
            end_date,
            service_dynamic_usage=service.service_dynamic_usage,
        )
        if staff_active_features.is_enabled('openstack.instances.traffic'):
            # TODO: check for feature inside the collect method
            collect_internal_usage(
                usage_data=usage,
                start=start_date,
                end=end_date,
                service_dynamic_usage=service.service_dynamic_usage,
            )
        add_pricing(usage, client, usage_settings=usage_settings)
        project = usage.get('project', None)
        if not project:
            return report
        report['service'] = service.id
        total_cost = usage.get('price', Decimal(0))
        report['total_cost'] = total_cost
        for usage_detail in usage.get('usage_details', []):
            resource_type = usage_detail.get('resource_type')
            resource_name = usage_detail.get('resource_name')
            for rtype_usage in usage_detail.get('usage', []):
                region = rtype_usage.get('region', default_region)
                region = region or default_region
                price = Decimal(rtype_usage.get('price', 0))
                if region not in location_details:
                    location_details[region] = {resource_type: {'resource_name': resource_name,
                                                                'price': price,
                                                                'num_resources': 1}}
                    report['location_cost'][region] = price
                elif resource_type not in location_details[region]:
                    location_details[region][resource_type] = {'resource_name': resource_name,
                                                               'price': price,
                                                               'num_resources': 1}
                    report['location_cost'][region] += price
                else:
                    location_details[region][resource_type]['price'] += price
                    location_details[region][resource_type]['num_resources'] += 1
                    report['location_cost'][region] += price
        report['locations'] = location_details
        report['total_cost'] = cdecimal(report['total_cost'], q='.01')
        return report

    def get_service_unsettled_periods(self, service: Service):
        unsettled_periods = []
        unsettled_periods_query = ServiceDynamicUsageHistory.objects.filter(
            state=ClientBillingStates.unsettled,
        )
        unsettled_periods_query = self.filter_service_usage_history(unsettled_periods_query, service)

        for unsettled_period in unsettled_periods_query:  # type: ServiceDynamicUsageHistory
            unsettled_period.state = ClientBillingStates.invoiced
            unsettled_period.save()
            unsettled_periods.append(unsettled_period)
        return unsettled_periods

    def change_pricing_plan(self, service: Service, new_plan_id):
        try:
            db_plan = PricingPlan.objects.get(pk=new_plan_id)
        except ObjectDoesNotExist:
            raise ObjectNotFound(detail=_('Pricing plan does not exist'))
        else:
            # TODO: see if this is correct
            if self.reseller_usage:
                service.reseller_service_dynamic_usage.plan = db_plan
                service.reseller_service_dynamic_usage.save(update_fields=['plan'])
            else:
                service.service_dynamic_usage.plan = db_plan
                service.service_dynamic_usage.save(update_fields=['plan'])
