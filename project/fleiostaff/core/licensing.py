import io
import json
import logging
import platform
import sys
import zipfile
from json import JSONDecodeError
from os import path, remove

import requests
import six
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _
from keystoneauth1.exceptions import ConnectFailure, ConnectTimeout, DiscoveryFailure, EndpointNotFound, Unauthorized
from novaclient.exceptions import ClientException
from rest_framework import exceptions

from fleio.conf.exceptions import ConfigException

try:
    from distro import linux_distribution
except ImportError:
    def linux_distribution():
        return '', '', ''

LOG = logging.getLogger(__name__)


def get_license_file(license_key):
    """Connect to licensing server."""
    dist = get_os_and_version()
    install_dir = path.dirname(path.dirname(path.dirname(__file__)))  # fleio install directory
    python_version = '{}.{}'.format(sys.version_info.major, sys.version_info.minor)
    if isinstance(dist, six.text_type):
        headers = {
            'User-Agent': r'Fleio\{0}\{1}\{2}\{3}\{4}'.format(dist, '', platform.machine(), install_dir,
                                                              python_version)}
    else:
        headers = {'User-Agent': r'Fleio\{0}\{1}\{2}\{3}\{4}'.format(dist[0], dist[1], platform.machine(), install_dir,
                                                                     python_version)}
    url = settings.LICENSING_SERVER_URL + 'moduleop/get-license-module-post'
    response = requests.post(url, stream=True, headers=headers,
                             data={'license_key': license_key, 'version': settings.FLEIO_BACKEND_VERSION},
                             proxies=settings.PROXY_SETTINGS, timeout=(10, 60))
    return response


def get_os_and_version():
    # linux
    dist = linux_distribution()  # (op_sys_name, op_sys_version, op_sys_code_name)
    if dist == ('', '', ''):
        try:
            with io.open("/etc/issue") as f:
                # linux arch, mac
                dist = f.read().lower().split()[0]
        except (IOError, OSError, ValueError):
            # maybe windows
            dist = '{} {}'.format(platform.system(), platform.release())
            if dist == ('', '', ''):
                raise exceptions.ParseError(detail=_('Your operating system information could not be found'))
    return dist


def extract_license(response, destination_path):
    """Receive and extract zip file."""
    with io.open('license.zip', 'wb+') as license_zip:
        license_zip.write(force_bytes(response.content))
    try:
        with zipfile.ZipFile('license.zip', mode='r') as license_zip:
            license_zip.extractall(destination_path)
    except zipfile.BadZipfile:
        raise exceptions.ParseError(detail=_('License file not intact. Please reactivate license'))
    except (IOError, OSError):
        raise exceptions.PermissionDenied(detail=_('Can\'t extract zip file. '
                                                   'Please allow write access and reactivate license.'))
    remove('license.zip')


def get_current_cores():
    if 'fleio.openstack' not in settings.INSTALLED_APPS:
        return 0

    from fleio.openstack.api.identity import IdentityAdminApi
    from fleio.openstack.api.nova import nova_client
    from fleio.openstack.models import OpenstackRegion

    physical_cores = 0
    for region in OpenstackRegion.objects.all():
        try:
            client = nova_client(api_session=IdentityAdminApi().session, region_name=region.id)
            for virtual_node in client.hypervisors.list():
                cpu_info = virtual_node.cpu_info
                if isinstance(cpu_info, str):
                    cpu_info = json.loads(cpu_info)
                physical_cores += int(cpu_info['topology']['cores'])
        except (ClientException, ConnectTimeout, Unauthorized, ConnectFailure, TypeError, JSONDecodeError,
                DiscoveryFailure):
            raise exceptions.APIException()
        except EndpointNotFound:
            # region not available
            LOG.error(
                'Region not found when attempting to get number of cores for region {}, ignoring'.format(region.id),
            )
        except ConfigException:
            # configuration error
            LOG.exception(
                'Invalid configuration when attempting to get number of cores for region {}, ignoring'.format(
                    region.id
                ),
            )
            # region not available
        except Exception as e:
            del e  # unused
            LOG.exception(
                'Exception when attempting to get number of cores for region {}, ignoring'.format(region.id),
            )
    return physical_cores
