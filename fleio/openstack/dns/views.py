import logging
from typing import Tuple

from designateclient import exceptions as designate_exceptions
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from keystoneauth1.exceptions import ClientException
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from fleio.billing.credit_checker import check_if_enough_credit
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack.api.designate import designate_client

from fleio.openstack.dns.utils import get_api_session, get_recordsets_changes, remove_unicode
from fleio.openstack.views.regions import get_regions
from .serializers import DnsSerializer
from .serializers import ListRecordsSerializer
from .serializers import RECORD_TYPES
from .serializers import SyncRecordSetsSerializer
from .serializers import DnsCreateSerializer
from .serializers import DnsFilterSerializer
from .serializers import DnsUpdateSerializer
from .serializers import RecordSetAlterSerializer
from .serializers import RecordSetCreateSerializer
from .serializers import RecordSetListSerializer
from fleio.openstack.dns.utils import create_or_update_ptr, get_ptr_from_ip

LOG = logging.getLogger(__name__)


def get_filter_params(request) -> Tuple[dict, int, dict]:
    params = {}
    name = None
    limit = None
    ordering = None

    # get custom filtering parameters
    custom_filtering_params = request.query_params.get('filtering', None)
    custom_filtering_params = custom_filtering_params.split('+') if custom_filtering_params else None
    if custom_filtering_params:
        client = None
        for filtering_param in custom_filtering_params:
            filtering_param = filtering_param.split(':')
            if filtering_param[0] == 'client':
                client = filtering_param[1]
        custom_filtering_params = dict(
            client=client
        )

    try:
        name = request.query_params['search']
    except (KeyError, ValueError):
        pass

    try:
        ordering = request.query_params['ordering']
    except (KeyError, ValueError):
        pass

    try:
        limit = int(request.query_params['page_size'])
        if limit > 1000:
            limit = 1000  # NOTE(tomo): designate requires less than 1000
    except (KeyError, ValueError):
        pass
    if name:
        params['name'] = '*{}*'.format(name)
    if ordering:
        if ordering[:1] == '-':
            params['sort_dir'] = 'desc'
            params['sort_key'] = ordering[1:]
        else:
            params['sort_dir'] = 'asc'
            params['sort_key'] = ordering
    return params, limit, custom_filtering_params


class DnsViewSet(viewsets.ViewSet):
    permission_classes = (CustomPermissions, EndUserOnly,)

    @action(detail=False, methods=['get'])
    def get_ptr_from_ip(self, request):
        ip = request.query_params.get('ip', None)
        region_name = request.query_params.get('region_name', None)
        try:
            response_dict = get_ptr_from_ip(ip=ip, region_name=region_name, request_session=request.session)
        except (designate_exceptions.Base, ClientException):
            raise ValidationError({
                'detail': _('Unable to get zone or record sets. Please contact support for more info')
            })
        except Exception as e:
            raise e
        return Response(response_dict)

    @action(detail=False, methods=['post'])
    def create_or_update_ptr(self, request):
        ip = request.data.get('ip', None)
        zone_id = request.data.get('zone_id', None)
        record = request.data.get('record', None)
        region_name = request.data.get('region_name', None)
        try:
            response_dict = create_or_update_ptr(
                ip=ip,
                zone_id=zone_id,
                record=record,
                region_name=region_name,
                request=request
            )
        except designate_exceptions.BadRequest:
            raise ValidationError({'detail': _('Not a valid domain name')})
        except (ClientException, designate_exceptions.Base, designate_exceptions.Conflict,
                designate_exceptions.RemoteError) as e:
            raise ValidationError({
                'detail': _('Unable to create or update ptr. Reason: {}. '
                            'Please contact support for more info.').format(str(e))
            })
        except Exception as e:
            raise ValidationError({'detail': _('An error occurred: {}').format(str(e))})
        return Response(response_dict, status=HTTP_201_CREATED)

    def list(self, request):
        """List all dns zones belonging to a region"""
        serializer = DnsFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=serializer.validated_data.pop('region_name', None))
        search_params, page_limit, custom_filtering_params = get_filter_params(request)
        criterion = {**search_params, **serializer.validated_data}

        try:
            zones = designate.zones.list(criterion=criterion, limit=page_limit)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('No zones found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to list zones, reason {0}'.format(e))
            raise ValidationError(detail=_('Unable to list zones. Please contact support for more info'))
        else:
            rsp = {'objects': DnsSerializer(instance=zones, many=True).data,
                   'permissions': permissions_cache.get_view_permissions(request.user, self.basename),
                   'hasMore': zones.next_page}
            return Response(rsp)

    @action(detail=True, methods=['get'])
    def list_records(self, request, pk=None):
        serializer = RecordSetListSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=serializer.validated_data.pop('region_name', None))

        try:
            serializer.validated_data['sort_key'] = 'type'
            recordsets = designate.recordsets.list(zone=pk, criterion=serializer.validated_data)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Zone not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to list records, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to list records. Please contact support for more info')})
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

        api_session = get_api_session(request)
        designate = designate_client(api_session)

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
            raise ValidationError({'detail': _('Unable to list records. Please contact support for more info')})
        else:
            response = ListRecordsSerializer(instance=recordsets).data
            response['record_types'] = [x[0] for x in RECORD_TYPES if x[0] != 'SOA']
            response['detail'] = _('Recordsets update scheduled')
            return Response(response)

    def create(self, request):
        """Create a dns zone"""

        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Failed to create DNS zone. Please contact support.'))

        serializer = DnsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=serializer.validated_data.pop('region_name', None))

        try:
            zone = designate.zones.create(**serializer.validated_data)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to create zone, reason {0}'.format(e))
            raise ValidationError({'detail': e})
        else:
            return Response(zone, status=HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        selected_region, regions = get_regions(request, for_end_user=True)
        return Response({
            'regions': regions,
            'selected_region': selected_region,
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            ),
        })

    @action(detail=True, methods=['post'])
    def create_records(self, request, pk=None):
        serializer = RecordSetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=serializer.validated_data.pop('region_name', None))

        try:
            records = designate.recordsets.create(zone=pk, **serializer.validated_data)
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to create record in zone {0}, reason {1}'.format(pk, e))
            raise ValidationError(detail=_('Unable to create record. Please contact support for more info'))
        else:
            return Response(records, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Fetches a dns zone"""
        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=request.query_params.get('region_name', None))

        try:
            zone = designate.zones.get(zone=pk)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Zone not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to fetch zone, reason {0}'.format(e))
            raise ValidationError(detail=_('Unable to fetch zone. Please contact support for more info'))

        return Response(DnsSerializer(instance=zone).data)

    @action(detail=True, methods=['get'])
    def retrieve_record(self, request, pk=None):
        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=request.query_params.get('region_name'))

        try:
            recordsets = designate.recordsets.get(zone=pk, recordset=request.query_params.get('pk'))
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Records not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to retrieve record, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to retrieve record. Please contact support for more info')})
        else:
            return Response(recordsets, status=HTTP_200_OK)

    def update(self, request, pk=None):
        """Updates a dns zone"""

        serializer = DnsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=serializer.validated_data.pop('region_name', None))

        try:
            zone = designate.zones.update(zone=pk, values=serializer.validated_data)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Zone not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to update zone, reason {0}'.format(e))
            raise ValidationError({'detail': e})
        else:
            return Response(zone, status=HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_record(self, request, pk=None):
        serializer = RecordSetAlterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=serializer.validated_data.pop('region_name', None))

        try:
            recordsets = designate.recordsets.update(zone=pk,
                                                     recordset=request.data.get('pk'),
                                                     values=serializer.validated_data)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Zone or record not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to update record, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to update record. Please contact support for more info')})
        else:
            return Response(recordsets, status=HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Delete a dns zone"""

        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=request.query_params.get('region_name', None))

        try:
            designate.zones.delete(zone=pk)
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Zone not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to delete zone, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to delete zone. Please contact support for more info')})
        else:
            return Response({'detail': _('Zone deleted')}, status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'])
    def delete_record(self, request, pk=None):
        api_session = get_api_session(request)
        designate = designate_client(api_session, region_name=request.data.get('region_name'))

        try:
            recordsets = designate.recordsets.delete(zone=pk, recordset=request.data.get('pk'))
        except (designate_exceptions.NotFound, designate_exceptions.ResourceNotFound) as e:
            LOG.error(e)
            raise NotFound(detail=_('Record not found'))
        except (designate_exceptions.Base, ClientException) as e:
            LOG.error('Unable to delete record, reason {0}'.format(e))
            raise ValidationError({'detail': _('Unable to delete record. Please contact support for more info')})
        else:
            return Response(recordsets, status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
