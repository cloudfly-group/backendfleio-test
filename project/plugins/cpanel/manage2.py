import logging
import ipaddress
from typing import Optional, Tuple

from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import Service
from fleio.billing.modules.universal import UniversalModule
from .api import Manage2Api, Manage2ApiException

LOG = logging.getLogger(__name__)


class Manage2Module(UniversalModule):
    module_name = 'cPanel Manage2 Module'

    def __init__(self):
        self.api = Manage2Api()

    def can_accept_order(self, service: Service) -> Tuple[bool, str]:
        try:
            module_settings = service.product.cpanel_plugin_settings
        except Exception as e:
            LOG.exception('Exception when attempting to get cpanel server product settings: {}'.format(e))
        else:
            if module_settings:
                del module_settings  # unused, retrieved only for test
                return True, ''

        return False, _('CPanel manage2 product is not properly configured.')

    def create(self, service: Service):
        if not service.product.cpanel_plugin_settings:
            LOG.error('cPanel manage2 plugin not configured for {}'.format(service.product.name))
            raise Manage2ApiException('Unable to activate license')
        license_ip = service.plugin_data.get('cpanel_license_ip')
        if not license_ip:
            raise Manage2ApiException('Unable to activate license without an IP')
        try:
            ipaddress.ip_address(license_ip)
        except ValueError:
            raise Manage2ApiException('Unable to activate license')

        package_id = service.product.cpanel_plugin_settings.cpanel_package_id
        group_id = service.product.cpanel_plugin_settings.cpanel_group_id
        response = self.api.add_license(ip=service.plugin_data.get('cpanel_license_ip'),
                                        package_id=package_id,
                                        group_id=group_id)
        internal_id = response.get('licenseid', None)
        return internal_id

    def suspend(self, service, reason=None, suspend_type=None):
        self.api.expire_license(license_id=service.internal_id)
        return True

    def resume(self, service: Service):
        return self.create(service=service)

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None):
        return self.suspend(service=service)
