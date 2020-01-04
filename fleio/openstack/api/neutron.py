from __future__ import absolute_import

import logging
from typing import List, Optional
from retrying import retry

from django.conf import settings

from neutronclient.v2_0.client import Client
from neutronclient.common.exceptions import Conflict

from fleio.openstack.api.nova import nova_client
from novaclient.client import exceptions
from fleio.openstack.settings import plugin_settings

LOG = logging.getLogger(__name__)


def neutron_client(api_session, region_name=None, service_type='network', version=None, interface=None):
    """
    Create the neutron client using the session object.
    :param version: the neutron client version (either explicit or the one in settings)
    :param api_session: Our Keystone Session wrapper
    :type api_session: keystoneauth1.session.Session
    :param str region_name: the region name
    :param str service_type: the neutron service type name as it appears in the service catalog
    :param str interface: the interface used for communication i.e public, private, admin
    :rtype: Client
    """

    region_name = region_name or plugin_settings.DEFAULT_REGION
    interface = interface or plugin_settings.DEFAULT_INTERFACE
    c = Client(session=api_session,
               interface=interface,
               version=version,
               region_name=region_name,
               service_type=service_type)
    return c


def create_security_group_if_missing(api_session, region=None, name=settings.SECURITY_GROUP_NAME,
                                     description=settings.SECURITY_GROUP_DESCRIPTION, project_id=None):
    sgid = None
    try:
        project_id = project_id or api_session.auth.get_access(api_session).project_id
        sgs_gen = neutron_client(api_session, region_name=region).list_security_groups(retrieve_all=False,
                                                                                       name=name,
                                                                                       tenant_id=project_id)
        for sgs in sgs_gen:
            for sg in sgs.get('security_groups', []):
                if sg['name'] == name:
                    sgid = sg['id']
                    break
    except Exception as e:
        LOG.exception(e)
        return

    if not sgid:
        sec_group = {'security_group': {'name': name,
                                        'description': description,
                                        # TODO(erno): if we begin to use openstack newton or higher change
                                        # this to project_id
                                        'tenant_id': project_id
                                        }
                     }
        sg = neutron_client(api_session, region_name=region).create_security_group(sec_group)
        sgid = sg['security_group']['id']
        rule_ipv4 = {'security_group_rule': {'direction': 'ingress',
                                             'remote_ip_prefix': '0.0.0.0/0',
                                             'security_group_id': sgid
                                             }
                     }
        rule_ipv6 = {'security_group_rule': {'direction': 'ingress',
                                             'remote_ip_prefix': '::/0',
                                             'ethertype': 'IPv6',
                                             'security_group_id': sgid
                                             }
                     }
        neutron_client(api_session, region_name=region).create_security_group_rule(rule_ipv4)
        neutron_client(api_session, region_name=region).create_security_group_rule(rule_ipv6)
    return sgid


def retry_if_result_is_falsy(result):
    return not result


@retry(retry_on_result=retry_if_result_is_falsy, wait_fixed=2000, stop_max_attempt_number=30)
def wait_for_instance_deleted(device_id, nova_c: nova_client):
    try:
        nova_c.servers.get(device_id)
    except exceptions.NotFound:
        return True
    return False


def delete_project_security_groups(api_session, project_id, region=None, instances_list: Optional[List] = None):
    neutron_cl = neutron_client(api_session, region_name=region)
    nova_c = nova_client(api_session=api_session, region_name=region)
    # wait for all instances to be gone first
    if instances_list:
        for instance_id in instances_list:
            wait_for_instance_deleted(device_id=instance_id, nova_c=nova_c)

    try:
        security_groups = neutron_cl.list_security_groups(fields=['id', 'name'],
                                                          tenant_id=project_id).get('security_groups', [])
        for security_group in security_groups:
            if security_group['name'] != 'default':
                try:
                    neutron_cl.delete_security_group(security_group['id'])
                except Conflict as e:
                    LOG.exception(e)  # should not get here because we waited for instances to disappear above
    except Exception as e:
        LOG.exception(e)
