import copy
import logging

from designateclient import exceptions as designate_exceptions

from keystoneauth1.exceptions import ClientException
from keystoneauth1.exceptions.catalog import EndpointNotFound

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from fleio.core.models import Client
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack.api.designate import designate_client
from fleio.openstack.api.identity import IdentityAdminApi, IdentityUserApi
from fleio.openstack.dns.serializers import ListRecordsSerializer, RECORD_TYPES, SyncRecordSetsSerializer, ZONE_TYPES
from fleio.openstack.dns.utils import remove_unicode
from fleio.openstack.dns.views import get_filter_params
from fleio.openstack.views.regions import get_regions

from .serializers import DnsCreateSerializer
from .serializers import DnsFilterSerializer
from .serializers import DnsSerializer
from .serializers import DnsUpdateSerializer
from .serializers import RecordSetCreateSerializer
from .serializers import RecordSetListSerializer
from .serializers import RecordSetUpdateSerializer

LOG = logging.getLogger(__name__)


class DnsViewSet(viewsets.ViewSet):
    permission_classes = (CustomPermissions, StaffOnly, )

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def list(self, request):
        """List all dns zones belonging to a region"""

        serializer = DnsFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        search_params, page_limit, custom_filtering_params = get_filter_params(request)
        all_projects = serializer.validated_data.pop('all_projects', None)

        # custom filtering by client
        custom_api_session = None
        client_id = custom_filtering_params.get('client', None) if custom_filtering_params else None
        if client_id:
            client = Client.objects.get(id=client_id)
            project = client.first_project
            if not project:
                raise APIBadRequest(_('Client you want zones for does not have an openstack project.'))
            custom_api_session = IdentityUserApi(
                project.project_id,
                project.project_domain_id,
                cache=request.session
            ).session
            all_projects = None

        designate = designate_client(self.identity_admin_api.session if not custom_api_session else custom_api_session,
                                     region_name=serializer.validated_data.pop('region_name', None),
                                     sudo_project_id=serializer.validated_data.pop('sudo_project_id', None),
                                     all_projects=all_projects)
        criterion = {**search_params, **serializer.validated_data}

        try:
            zones = designate.zones.list(criterion=criterion, limit=page_limit)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('No zones found'))
        except designate_exceptions.Base as e:
            LOG.error('Unable to list zones, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to list zones. Please see logs for more info')})
        except EndpointNotFound as e:
            LOG.error('Endpoint not found: {}'.format(e))
            raise NotFound(detail=_('DSN endpoint not found'))
        else:
            rsp = {'objects': DnsSerializer(instance=zones, many=True).data,
                   'count': len(zones),
                   'hasMore': zones.next_page}
            return Response(rsp)

    @action(detail=True, methods=['get'])
    def list_records(self, request, pk=None):
        serializer = RecordSetListSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        recordset_default_limit = getattr(settings, 'OPENSTACK_DESIGNATE_RECORDSET_LIMIT', 100000)
        records_limit = serializer.validated_data.pop('limit', recordset_default_limit)

        designate = designate_client(self.identity_admin_api.session,
                                     region_name=serializer.validated_data.pop('region_name', None),
                                     all_projects=serializer.validated_data.pop('all_projects', None))

        try:
            serializer.validated_data['sort_key'] = 'type'
            recordsets = designate.recordsets.list(zone=pk, criterion=serializer.validated_data, limit=records_limit)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Zone not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to list records, reason {0}'.format(e))
            raise ValidationError({'detail': str(e)})
        else:
            response = ListRecordsSerializer(instance=recordsets).data
            response['record_types'] = [x[0] for x in RECORD_TYPES if x[0] != 'SOA']
            return Response(response)

    @action(detail=True, methods=['post'])
    def synchronize_records(self, request, pk):
        serializer = SyncRecordSetsSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        current_recordsets = serializer.validated_data
        for recordset_i in current_recordsets:
            for recordset_j in current_recordsets:
                if recordset_i['id'] == recordset_j['id']:
                    continue
                if recordset_i['name'] == recordset_j['name'] and recordset_i['type'] == recordset_j['type']:
                    raise ValidationError({'detail': _('More than one recordset exists with the same subdomain '
                                                       '{subd} and type {type} exist'
                                                       .format(subd=recordset_i['name'], type=recordset_i['type']))})

        designate = designate_client(self.identity_admin_api.session, all_projects=True, edit_managed=True)

        try:
            recordset_default_limit = getattr(settings, 'OPENSTACK_DESIGNATE_RECORDSET_LIMIT', 100000)
            existing_recordsets = designate.recordsets.list(zone=pk, limit=recordset_default_limit)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to list records, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to list records. Please contact support for more info')})

        # create, update and delete recordsets
        create_recordsets, update_recordsets, delete_recordsets = \
            get_recordsets_changes(current_recordsets, existing_recordsets)

        # TODO(erno): make a celery task for this, refactor frontend too
        errors = {}
        create_errors = ''
        for recordset in create_recordsets:
            try:
                designate.recordsets.create(zone=pk, name=recordset['name'], type_=recordset['type'],
                                            records=recordset['records'], ttl=recordset['ttl'])
            except (designate_exceptions.Base, ClientException) as e:
                create_errors += '{}\n'.format(remove_unicode(str(e)))
        if create_errors:
            errors['detail'] = create_errors

        for recordset in update_recordsets:
            try:
                designate.recordsets.update(zone=pk, recordset=recordset['id'],
                                            values={'records': recordset['records'], 'ttl': recordset['ttl']})
            except (designate_exceptions.Base, ClientException) as e:
                errors[recordset['id']] = remove_unicode(str(e))

        for record_id in delete_recordsets:
            try:
                designate.recordsets.delete(zone=pk, recordset=record_id)
            except (designate_exceptions.Base, ClientException) as e:
                errors[record_id] = remove_unicode(str(e))

        if errors:
            raise ValidationError(errors)

        try:
            recordsets = designate.recordsets.list(zone=pk)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to list records, reason {0}'.format(e))
            raise ValidationError({'detail': str(e)})
        else:
            response = ListRecordsSerializer(instance=recordsets).data
            response['record_types'] = [x[0] for x in RECORD_TYPES if x[0] != 'SOA']
            response['detail'] = _('Recordsets update scheduled')
            return Response(response)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        selected_region, regions = get_regions(request)
        return Response({'regions': regions, 'selected_region': selected_region, 'types': ZONE_TYPES})

    def create(self, request):
        """Create a dns zone"""

        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))

        serializer = DnsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        designate = designate_client(self.identity_admin_api.session,
                                     region_name=serializer.validated_data.pop('region_name', None),
                                     sudo_project_id=serializer.validated_data.pop('sudo_project_id', None),
                                     all_projects=serializer.validated_data.pop('all_projects', None))
        serializer.validated_data.pop('client', None)
        try:
            zone = designate.zones.create(**serializer.validated_data)
        except designate_exceptions.Conflict as e:
            LOG.error('Unable to create zone, reason {0}'.format(e))
            raise ValidationError(
                {'detail': _('Unable to create zone. A zone with the same domain name already exists')}
            )
        except designate_exceptions.Base as e:
            LOG.error('Unable to create zone, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to create zone. Please see logs for more info')})
        else:
            return Response(zone, status=HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def create_records(self, request, pk=None):
        serializer = RecordSetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        designate = designate_client(self.identity_admin_api.session,
                                     region_name=serializer.validated_data.pop('region_name', None,),
                                     sudo_project_id=serializer.validated_data.pop('sudo_project_id', None))

        try:
            records = designate.recordsets.create(zone=pk, **serializer.validated_data)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to create record in zone {0}, reason {1}'.format(pk, e))
            raise ValidationError({'detail': _('Unable to create record. Please see logs for more info')})
        else:
            return Response(records, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Fetches a dns zone"""

        designate = designate_client(self.identity_admin_api.session,
                                     region_name=request.query_params.get('region_name', None),
                                     sudo_project_id=request.query_params.get('sudo_project_id', None),
                                     all_projects=request.query_params.get('all_projects', True))

        try:
            zone = designate.zones.get(zone=pk)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to fetch zone, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to fetch zone. Please see logs for more info')})
        return Response(DnsSerializer(instance=zone).data)

    @action(detail=True, methods=['get'])
    def retrieve_record(self, request, pk=None):

        designate = designate_client(self.identity_admin_api.session,
                                     region_name=request.query_params.get('region_name'),
                                     all_projects=request.query_params.get('all_projects'))

        try:
            recordsets = designate.recordsets.get(zone=pk, recordset=request.query_params.get('pk'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to retrieve record, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to retrieve record. Please see logs for more info')})
        else:
            return Response(recordsets, status=HTTP_200_OK)

    def update(self, request, pk=None):
        """Updates a dns zone"""
        serializer = DnsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        designate = designate_client(self.identity_admin_api.session,
                                     region_name=serializer.validated_data.pop('region_name', None),
                                     sudo_project_id=serializer.validated_data.pop('sudo_project_id', None),
                                     all_projects=serializer.validated_data.pop('all_projects', None))

        try:
            zone = designate.zones.update(zone=pk, values=serializer.validated_data)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to update zone, reason {0}'.format(e))
            raise ValidationError({'detail': e})
        else:
            return Response(zone, status=HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_record(self, request, pk=None):
        serializer = RecordSetUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        designate = designate_client(self.identity_admin_api.session,
                                     region_name=serializer.validated_data.pop('region_name', None),
                                     all_projects=serializer.validated_data.pop('all_projects', None))

        try:
            recordsets = designate.recordsets.update(zone=pk,
                                                     recordset=request.data.get('pk'),
                                                     values=serializer.validated_data)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to update record, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to update record. Please see longs for more info')})
        else:
            return Response(recordsets, status=HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Delete a dns zone"""
        designate = designate_client(self.identity_admin_api.session,
                                     region_name=request.query_params.get('region_name', None),
                                     all_projects=True)

        try:
            designate.zones.delete(zone=pk)
        except designate_exceptions.Base as e:
            LOG.error('Unable to delete zone, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to delete zone. Please see logs for more info')})
        else:
            return Response({'detail': _('Zone deleted')}, status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'])
    def delete_record(self, request, pk=None):
        designate = designate_client(self.identity_admin_api.session,
                                     region_name=request.query_params.get('region_name'),
                                     all_projects=request.query_params.get('all_projects'))

        try:
            recordsets = designate.recordsets.delete(zone=pk, recordset=request.query_params.get('pk'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to delete record, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to delete record. Please see logs for more info')})
        else:
            return Response(recordsets, status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)


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
