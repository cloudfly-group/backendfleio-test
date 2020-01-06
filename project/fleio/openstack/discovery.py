import logging
import requests
from django.utils.functional import cached_property
from keystoneauth1 import exceptions
from keystoneauth1.discover import get_version_data, normalize_version_number, version_match


class PublicEndpoint(object):
    """
    An endpoint from the service catalog based on given parameters.
    :param service_type: e.g.: compute, identity, etc.
    :param version: e.g.: 2.0, 2.12
    :param exact_match: If True give only then back the endpoint url if version exactly matches with the version of the
    endpoint, else check for compatible versions too. A version is compatible with another if the major version number
    is the same, and minor version number is greater or equal than the version supplied.
    """
    @cached_property
    def endpoints_catalog(self):
        service_catalog = self.api_session.auth.get_access(self.api_session).service_catalog
        endpoints = service_catalog.get_endpoints()
        return endpoints

    def __init__(self, api_session, service_type, desired_version=None, exact_match=False):
        self.api_session = api_session
        self.service_type = service_type
        self.desired_version = desired_version
        self.exact_match = exact_match

    def _get_raw_endpoint_url(self):
        items = []
        for endpoint in self.endpoints_catalog:
            if self.service_type == endpoint:
                for item in self.endpoints_catalog[endpoint]:
                    if item['interface'] == 'public':
                        # there can be more than one public interface if the OpenStack is multi-region
                        items.append(item)
        return items

    def _get_ip_and_port(self, item):
        url_split = item['url'].split('/')
        if ':' not in url_split[2] and len(url_split) > 3:
            return url_split[0] + '//' + url_split[2] + '/' + url_split[3]
        # TODO(erno): refactor if openstack version supported will be >= pike
        return url_split[0] + '//' + url_split[2]

    def _parse_json_endpoints(self, item, response):
        try:
            data = response.json()
            if 'values' in data['versions']:
                data['versions'] = data['versions']['values']
            versions = data['versions']
        except (KeyError, TypeError, SyntaxError, ValueError) as e:
            del e  # unused
            try:
                versions = get_version_data(session=self.api_session, url=item['url'])
            except (exceptions.DiscoveryFailure, exceptions.NotFound, Exception) as e:
                logging.error('{} - {}'.format(item.get('url', ''), str(e)))
                return None
        return versions

    @cached_property
    def endpoint_with_versions(self):
        """Get the endpoint with versions matching service_type and interface"""

        items = self._get_raw_endpoint_url()

        if not items:
            return None
        else:
            versions = []
            for item in items:
                url = self._get_ip_and_port(item)
                try:
                    json_response_endpoints = requests.get(url, timeout=3, verify=self.api_session.verify)
                except requests.exceptions.ReadTimeout:
                    return None
                else:
                    versions.append(self._parse_json_endpoints(item, json_response_endpoints))

        return versions

    def unvalidated_endpoint_url(self, region):
        """Get the endpoint url found for the given parameters without performing any validation, or return None"""
        items = self._get_raw_endpoint_url()

        for item in items:
            if item['region_id'] == region:
                return self._get_ip_and_port(item)

        return None

    @cached_property
    def version_data(self):
        """Get an endpoint with its versions"""
        all_version_data = []

        if not self.endpoint_with_versions:
            return None
        else:
            for endpoint in self.endpoint_with_versions:

                if not endpoint:
                    continue

                for version in endpoint:
                    if not self.desired_version:
                        if 'version' in version and version['version']:
                            all_version_data.append(version)
                        elif 'id' in version:
                            all_version_data.append(version)
                    else:
                        if 'version' in version and version['version']:
                            if self.exact_match:
                                if version['version'] == str(self.desired_version):
                                    all_version_data.append(version)
                            else:
                                current_micro_version = normalize_version_number(version['version'])
                                required_micro_version = normalize_version_number(str(self.desired_version))
                                if version_match(required_micro_version, current_micro_version):
                                    all_version_data.append(version)
                        elif 'id' in version and version["id"]:
                            if self.exact_match:
                                if version['id'] == 'v' + str(self.desired_version):
                                    all_version_data.append(version)
                            else:
                                current_version = normalize_version_number(version['id'])
                                required_version = normalize_version_number(str(self.desired_version))
                                if version_match(required_version, current_version):
                                    all_version_data.append(version)
            return all_version_data

    @cached_property
    def endpoint_url(self):
        """Get the endpoint url found for the given parameters, or return None"""
        urls = []
        if not self.version_data:
            return None
        else:
            for endpoint in self.version_data:
                urls.append(endpoint['links'][0]['href'])
        return urls

    @cached_property
    def version(self):
        """Get the version found for the given parameters, or return None"""
        if not self.version_data:
            return None
        else:
            versions = []
            if self.desired_version:
                for endpoint in self.version_data:
                    if 'version' in endpoint and endpoint['version'] == str(self.desired_version):
                        versions.append(endpoint['version'])
                    elif 'id' in endpoint and endpoint['id'] == 'v' + str(self.desired_version):
                        versions.append(endpoint['id'])
            else:
                for endpoint in self.version_data:
                    if 'version' in endpoint and endpoint['version']:
                        versions.append(endpoint['version'])
                    elif 'id' in endpoint and endpoint['id']:
                        versions.append(endpoint['id'])
            return versions
