import logging
import copy
import re

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ipaddress import ip_address
from ipaddress import IPv6Address

from designateclient import exceptions as designate_exceptions
from keystoneauth1.exceptions import ClientException

from fleio.openstack.api.designate import designate_client
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.core.exceptions import APIConflict
from fleio.openstack.api.identity import IdentityUserApi
from fleio.openstack.dns.serializers import CreateOrUpdatePtrSerializer, GetPtrFromIpSerializer

LOG = logging.getLogger(__name__)


def fetch_project(request):
    """Returns openstack project for the first client of request.user or throws exceptions"""

    # TODO(Marius): as soon as a client supports multiple projects, implement a create options
    #  view which will return the available projects to select from and also a list of roles
    client = request.user.clients.filter(services__openstack_project__isnull=False).first()

    if client is None:
        raise APIConflict(_('No client with an OpenStack project found'))

    return client.first_project


# TODO: move this in some common place
def get_api_session(request):
    project = fetch_project(request)
    project_id, project_domain_id = project.project_id, project.project_domain_id
    os_api = IdentityUserApi(project_id,
                             project_domain_id,
                             cache=request.session)
    return os_api.session


def get_recordsets_changes(current_recordsets, existing_recordsets):
    """
    Compare data from openstack and records coming from request to identify the minimal operations necessary
    to syncronize openstack recordsets with current data
    """
    update_recordsets = []
    delete_recordsets = []
    del_recordsets = [recordset for recordset in current_recordsets if recordset['deleted']]
    crea_upd_recordsets = [recordset for recordset in current_recordsets if not recordset['deleted']]
    crea_upd_recordsets2 = copy.deepcopy(crea_upd_recordsets)
    exist_recordsets = copy.deepcopy(existing_recordsets)
    exist_recordsets2 = copy.deepcopy(existing_recordsets)

    # process the deleted recordsets
    for del_r in del_recordsets:
        for exist_r in exist_recordsets:
            if del_r['id'] == exist_r['id']:
                delete_recordsets.append(exist_r['id'])
                exist_recordsets2.remove(exist_r)
            elif del_r['name'] == exist_r['name'] and del_r['type'] == exist_r['type']:
                delete_recordsets.append(exist_r['id'])
                exist_recordsets2.remove(exist_r)

    exist_recordsets = copy.deepcopy(exist_recordsets2)

    # process the updated recordsets
    for curr_r in crea_upd_recordsets:
        for exist_r in exist_recordsets:
            if curr_r['id'] == exist_r['id']:
                if curr_r['records'] != exist_r['records'] or curr_r['ttl'] != exist_r['ttl']:
                    update_recordsets.append(curr_r)
                crea_upd_recordsets2.remove(curr_r)
            # is unique together in recordset list for a zone
            elif curr_r['name'] == exist_r['name'] and curr_r['type'] == exist_r['type']:
                crea_upd_recordsets2.remove(curr_r)
                if curr_r['records'] != exist_r['records']:
                    curr_r['id'] = exist_r['id']
                    update_recordsets.append(curr_r)

    # since we processed the deleted and updated recordsets the remaining recordsets can only be created
    return crea_upd_recordsets2, update_recordsets, delete_recordsets


def remove_unicode(string):
    return re.sub(r"u('.*?')", r"\1", string)


def get_ptr_from_ip(ip, region_name, request_session=None) -> dict:
    params = {
        'ip': ip,
        'region_name': region_name
    }
    serializer = GetPtrFromIpSerializer(data=params)
    serializer.is_valid(raise_exception=True)

    if request_session:
        designate = designate_client(api_session=IdentityAdminApi(request_session=request_session).session,
                                     region_name=serializer.validated_data.pop('region_name', None))
    else:
        designate = designate_client(api_session=IdentityAdminApi().session,
                                     region_name=serializer.validated_data.pop('region_name', None))

    related_ip = ip_address(serializer.validated_data['ip'])
    ptr_record = related_ip.reverse_pointer + '.'
    if isinstance(related_ip, IPv6Address):
        zone_name = ptr_record
    else:
        # cut the first segment (last segment from the ip)
        zone_name = ptr_record[ptr_record.index('.') + 1:]
    try:
        zones = designate.zones.list(criterion={'name': zone_name})
    except (designate_exceptions.Base, ClientException) as e:
        raise e

    if zones:
        zone_id = zones[0]['id']
        try:
            recordsets = designate.recordsets.list(zone=zone_id, criterion={'type': 'PTR', 'name': ptr_record})
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to list record sets, reason {0}'.format(e))
            raise e
        if recordsets:
            # TODO(erno): returns only the first PTR entry, and the first record
            record = recordsets[0]['records'][0]
            if record.endswith('.'):
                record = record[:-1]
            return dict(record=record, zone_id=zone_id,)
        else:
            dict(record='', zone_id=zone_id,)

    return dict(record='', zone_id='',)


def create_or_update_ptr(ip, record, region_name, zone_id=None, request=None):
    data = dict(
        ip=ip,
        record=record,
        region_name=region_name,
    )
    if zone_id:
        data['zone_id'] = zone_id
    serializer = CreateOrUpdatePtrSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    if request:
        designate = designate_client(api_session=IdentityAdminApi(request_session=request.session).session,
                                     region_name=serializer.validated_data.pop('region_name', None))
    else:
        designate = designate_client(api_session=IdentityAdminApi().session,
                                     region_name=serializer.validated_data.pop('region_name', None))

    try:
        zone_id, created = get_or_create_zone(designate=designate, request=request, data=data)
    except (designate_exceptions.Base, designate_exceptions.RemoteError) as e:
        raise e

    record = serializer.validated_data['record']
    if not record.endswith('.'):
        record += '.'

    # update or create PTR record
    if created:
        recordset_name = ip_address(serializer.validated_data['ip']).reverse_pointer + '.'
        try:
            record = designate.recordsets.create(zone=zone_id, records=[record],
                                                 name=recordset_name, type_='PTR')
        except (designate_exceptions.BadRequest, ClientException) as e:
            raise e
    else:
        try:
            ptr_record = ip_address(serializer.validated_data['ip']).reverse_pointer + '.'
            recordsets = designate.recordsets.list(zone=zone_id, criterion={'type': 'PTR', 'name': ptr_record})
        except designate_exceptions.Base as e:
            LOG.error('Unable to list record sets, reason {0}'.format(e))
            raise e
        try:
            if recordsets:
                record = designate.recordsets.update(zone=zone_id, recordset=recordsets[0]['id'],
                                                     values={'records': [record]})
            else:
                recordset_name = ip_address(serializer.validated_data['ip']).reverse_pointer + '.'
                record = designate.recordsets.create(zone=zone_id, records=[record], name=recordset_name, type_='PTR')
        except (designate_exceptions.BadRequest, ClientException, designate_exceptions.Conflict) as e:
            raise e

    return dict(
        record=record
    )


def get_or_create_zone(designate, data: dict, request=None):
    created = False
    serializer = CreateOrUpdatePtrSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    related_ip = ip_address(serializer.validated_data['ip'])
    if 'zone_id' not in serializer.validated_data:
        ptr_record = related_ip.reverse_pointer + '.'
        if isinstance(related_ip, IPv6Address):
            zone_name = ptr_record
        else:
            # cut the first segment (last segment from the ip)
            zone_name = ptr_record[ptr_record.index('.') + 1:]
        try:
            zones = designate.zones.list(criterion={'name': zone_name})
            if zones:
                zone_id = zones[0]['id']
            else:
                if request:
                    client = request.user.clients.filter(services__openstack_project__isnull=False).first()
                    zone_id = designate.zones.create(name=zone_name, email=client.email)['id']
                else:
                    zone_id = designate.zones.create(
                        name=zone_name,
                        email=getattr(settings, 'INVERSE_ADDRESS_ZONE_DEFAULT_EMAIL', 'dummy@email.com')
                    )['id']
                created = True
        except (designate_exceptions.Base, ClientException) as e:
            raise e
    else:
        zone_id = serializer.validated_data['zone_id']
    return zone_id, created


def get_default_ptr_format(ip: str):
    if isinstance(ip_address(ip), IPv6Address):
        ptr_format = getattr(settings, 'PTR_DEFAULT_FORMAT_IPV6', None)  # type: str
        if ptr_format is None:
            return ptr_format
        dashed_ip = ip.replace(':', '-')
        return ptr_format.format(dashed_ip=dashed_ip)
    else:
        ptr_format = getattr(settings, 'PTR_DEFAULT_FORMAT', None)  # type: str
        if ptr_format is None:
            return ptr_format
        dashed_ip = ip.replace('.', '-')
        return ptr_format.format(dashed_ip=dashed_ip)
