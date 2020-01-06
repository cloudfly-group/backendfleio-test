import logging

from celery.canvas import Signature
from datetime import datetime
from decimal import Decimal
from typing import Optional

from plugins.hypanel.tasks import delete_hypanel_task
from plugins.hypanel.utils import get_hypanel_server_settings, send_hypanel_request

from fleio.billing.modules.base import ServiceUsage
from fleio.billing.usage_settings import UsageSettings
from fleio.billing.estimated_usage import EstimatedUsage

from fleio.billing.models import ConfigurableOption  # noqa
from fleio.billing.models import Service
from fleio.billing.models import ServiceConfigurableOption  # noqa
from fleio.servers.models import Server  # noqa
from fleio.core.models import Client  # noqa
from fleio.billing.modules.base import ModuleBase
from fleio.billing.settings import ServiceSuspendType


LOG = logging.getLogger(__name__)


class HypanelModule(ModuleBase):
    module_name = "Hypanel Module"

    def initialize(self, service: Service) -> bool:
        """Initializes a new service object.
        This should be the first function called on a service.

        Keyword arguments:
            service -- the service to initialize
        Returns:
            True if service was initialized successfully
        """
        LOG.debug('Hypanel module initialized called for service {}:{}'.format(service.id, service))
        return True

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        LOG.debug('{} delete called for service {}:{}'.format(self.module_name, service.id, service))
        hypanel_server = service.product.hypanel_product_settings.hypanel_server  # type: Server
        return delete_hypanel_task.si(service_id=service.id, **{
            'hypanel_server_settings': get_hypanel_server_settings(hypanel_server),
            'billing_client_id': service.client.id,
        })

    def create(self, service: Service) -> bool:
        LOG.debug('Hypanel module create called for service {}:{}'.format(service.id, service))
        module_settings = service.product.hypanel_product_settings
        hypanel_server = module_settings.hypanel_server  # type: Server
        hypanel_server_settings = get_hypanel_server_settings(hypanel_server)
        client = service.client  # type: Client
        params = {
            'billing_client_id': client.id,
            'accountid': service.id,  # accountid is actually the service id
            'firstname': client.first_name,
            'lastname': client.last_name,
            'email': client.email,
            'hostname': module_settings.hostname,
            'user': 'root',
            'server_group': module_settings.server_group,
            'ip_count': module_settings.ip_count,
            'configuration': module_settings.configuration,
            'memory': module_settings.memory,
            'disk_size': module_settings.disk_size,
            'traffic': module_settings.traffic,
            'machine_type': module_settings.machine_type,
            'send_welcome_email': module_settings.send_welcome_email,
        }
        # update the product params with configurable option settings
        conf_opts_dict = dict()
        for service_conf_opt in service.configurable_options.all():  # type: ServiceConfigurableOption
            option = service_conf_opt.option  # type: ConfigurableOption
            if option.name == 'hypanel_os':
                conf_opts_dict['os'] = service_conf_opt.option_value
            if option.name == 'hypanel_ip_count' and service_conf_opt.option_value:
                conf_opts_dict['ip_count'] = service_conf_opt.option_value
            if option.name == 'hypanel_control_panel' and service_conf_opt.option_value:
                conf_opts_dict['control_panel'] = service_conf_opt.option_value
        params.update(conf_opts_dict)
        # make the request
        response = send_hypanel_request(
            hypanel_server_settings=hypanel_server_settings,
            method='create_machine',
            params=params
        )
        if response.status_code == 200:
            return True
        return False

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None, ) -> bool:
        LOG.debug('Hypanel module suspend called for service {}:{}'.format(service.id, service))
        module_settings = service.product.hypanel_product_settings
        hypanel_server = module_settings.hypanel_server  # type: Server
        hypanel_server_settings = get_hypanel_server_settings(hypanel_server)
        client = service.client  # type: Client
        response = send_hypanel_request(
            hypanel_server_settings=hypanel_server_settings,
            method='suspend_machine',
            params={
                'billing_client_id': client.id,
                'billing_service_id': service.id,
            }
        )
        if response.status_code == 200:
            return True
        return False

    def resume(self, service: Service) -> bool:
        LOG.debug('Hypanel module resume called for service {}:{}'.format(service.id, service))
        module_settings = service.product.hypanel_product_settings
        hypanel_server = module_settings.hypanel_server  # type: Server
        hypanel_server_settings = get_hypanel_server_settings(hypanel_server)
        client = service.client  # type: Client
        response = send_hypanel_request(
            hypanel_server_settings=hypanel_server_settings,
            method='unsuspend_machine',
            params={
                'billing_client_id': client.id,
                'billing_service_id': service.id,
            }
        )
        if response.status_code == 200:
            return True
        return False

    def renew(self, service: Service) -> bool:
        pass

    def change_product(self, service: Service) -> bool:
        LOG.debug('{} change product called for service {}:{}'.format(self.module_name, service.id, service))
        module_settings = service.product.hypanel_product_settings
        hypanel_server = module_settings.hypanel_server  # type: Server
        hypanel_server_settings = get_hypanel_server_settings(hypanel_server)
        client = service.client  # type: Client

        params = {
            'billing_client_id': client.id,
            'billing_service_id': service.id,
            'newconf': module_settings.configuration,
            'memory': module_settings.memory,
            'disk_size': module_settings.disk_size,
            'traffic': module_settings.traffic,
            'ip_count': module_settings.ip_count,
        }
        # update the product params with configurable option settings
        conf_opts_dict = dict()
        for service_conf_opt in service.configurable_options.all():  # type: ServiceConfigurableOption
            option = service_conf_opt.option  # type: ConfigurableOption
            if option.name == 'hypanel_ip_count' and service_conf_opt.option_value:
                conf_opts_dict['ip_count'] = service_conf_opt.option_value
            if option.name == 'hypanel_control_panel' and service_conf_opt.option_value:
                conf_opts_dict['control_panel'] = service_conf_opt.option_value
        params.update(conf_opts_dict)
        # make the request
        response = send_hypanel_request(
            hypanel_server_settings=hypanel_server_settings,
            method='change_machine',
            params=params
        )
        if response.status_code == 200:
            return True
        return False

    def change_cycle(self, service: Service) -> bool:
        return True

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        return ServiceUsage(Decimal(0))

    def get_unpaid_usage(self, service: Service) -> ServiceUsage:
        return ServiceUsage(Decimal(0))

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        return EstimatedUsage()

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        return True

    def reset_usage(self, service: Service) -> bool:
        return True

    def settle_usage(self, service: Service, end_datetime: datetime) -> bool:
        return True

    def get_usage_summary(self, service: Service):
        pass

    def get_billing_summary(self, service: Service):
        pass

    def change_pricing_plan(self, service: Service, new_plan_id):
        pass
