import logging
import requests
from requests.exceptions import BaseHTTPError
from django.conf import settings

LOG = logging.getLogger(__name__)

API_URL = 'https://manage2.cpanel.net'


class CPanelExpirationCodes:
    normal = 'normal'
    nocomplete = 'nocomplete'
    noverify = 'noverify'
    shutoff = 'shutoff'
    chargeback = 'chargeback'
    fraud = 'fraud'
    other = 'other'


class Manage2ApiException(Exception):
    pass


class Manage2Api:
    ExpirationCodes = CPanelExpirationCodes

    def __init__(self):
        self.username = getattr(settings, 'CPANEL_USERNAME', None)
        self.password = getattr(settings, 'CPANEL_PASSWORD', None)
        if self.username is None or self.password is None:
            LOG.error('CPANEL_USERNAME or CPANEL_PASSWORD is not set in settings.py')

    def api_call(self, url, params=None):
        params = params or {}
        params['output'] = 'json'

        try:
            response = requests.get('{}/{}'.format(API_URL, url), params=params, auth=(self.username, self.password))
        except BaseHTTPError as e:
            raise Manage2ApiException(e)

        json_response = response.json()
        if json_response['status'] != 1:
            raise Manage2ApiException(json_response.get('reason', 'Unknown'))
        return json_response

    def add_license(self, ip, package_id, group_id):
        params = {'ip': ip,
                  'packageid': package_id,
                  'groupid': group_id}
        return self.api_call('XMLlicenseAdd.cgi', params=params)

    def change_license_ip(self, old_ip, new_ip, package_id, force=1, dry_run=0):
        parameters = {'oldip': old_ip,
                      'newip': new_ip,
                      'packageid': package_id,
                      'force': force}
        if dry_run:
            parameters['dryrun'] = 1
        return self.api_call('XMLtransfer.cgi', params=parameters)

    def expire_license(self, license_id, expiration_code='normal', reason=None):
        params = {'liscid': license_id,
                  'reason': reason,
                  'expcode': expiration_code}
        return self.api_call('XMLlicenseExpire.cgi', params=params)

    def reactivate(self, license_id, force=0, dry_run=0):
        params = {'liscid': license_id}
        if force:
            params['force'] = 1
        if dry_run:
            params['dryrun'] = 1
        return self.api_call('XMLlicenseReActivate.cgi', params=params)

    def list_licenses(self):
        return self.api_call('XMLlicenseInfo.cgi')

    def list_groups(self):
        return self.api_call('XMLgroupInfo.cgi')

    def list_packages(self):
        return self.api_call('XMLpackageInfo.cgi')

    def find_license_by_ip(self, ip, package_id=None, all_licenses=0):
        parameters = {'ip': ip}
        if package_id:
            parameters['packageid'] = package_id
        if all_licenses:
            parameters['all'] = all_licenses
        return self.api_call('XMLRawlookup.cgi', params=parameters)

    def get_license(self, ip, package_id=None, all_licenses=1):
        params = dict(ip=ip)
        params['all'] = all_licenses
        if package_id is not None:
            params['packageid'] = package_id
        return self.api_call('XMLRawlookup.cgi', params=params)
