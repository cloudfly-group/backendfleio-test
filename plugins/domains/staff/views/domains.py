from collections import OrderedDict

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY

from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from fleio.billing.settings import ServiceStatus
from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter
from fleio.core.models import Client
from fleio.reseller.utils import reseller_suspend_instead_of_terminate
from plugins.domains.exceptions import ApiDomainExpectationFailed

from plugins.domains.models import Domain
from plugins.domains.models import Nameserver
from plugins.domains.models import Registrar
from plugins.domains.models.domain import DomainStatus

from plugins.domains.registrars_connectors.registrar_connector_base import DomainActions
from plugins.domains.registrars_connectors.registrar_connector_manager import registrar_connector_manager

from plugins.domains.staff.serializers import DomainSerializer
from plugins.domains.staff.serializers import SaveNameserversSerializer
from plugins.domains.utils.domain import DomainUtils


class DomainsViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly, )
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, CustomFilter)
    search_fields = ('name', )
    ordering_fields = ('name', 'created_at', 'status', 'tld')

    @action(detail=False, methods=['get'])
    def create_options(self, request: Request) -> Response:
        del request  # unused

        create_options = {
            'statuses': [
                {
                    'status': domain_status,
                    'status_display': status_display
                } for domain_status, status_display in DomainStatus.domain_status_map.items()
            ]
        }

        return Response(create_options)

    @action(detail=False, methods=['get'])
    def get_client_domains(self, request: Request) -> Response:
        client_id = request.query_params.get('client_id', None)
        client = Client.objects.filter(id=client_id).first()

        if client:
            domains_for_client = Domain.objects.filter(service__client=client).order_by('-created_at')
            page = self.paginate_queryset(domains_for_client)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(domains_for_client, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': _('Client not found')}, status=HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=True, methods=['get'])
    def get_info(self, request: Request, pk) -> Response:
        del pk  # unused

        domain = self.get_object()
        registrar_id = request.query_params.get('registrar_id', None)
        registrar = Registrar.objects.filter(id=registrar_id).first() if registrar_id else None

        if registrar:
            registrar_connector = registrar_connector_manager.get_connector_instance(registrar.connector.name)
            actions = registrar_connector.get_domain_actions(domain=domain)
            if not actions:
                actions = []
            return Response(
                data={
                    'actions': [
                        {
                            'name': action_name,
                            'display_name': DomainActions.domain_actions_map[action_name],
                        } for action_name in actions
                    ],
                    'custom_fields': {
                        'cnp': {
                            'label': 'CNP',
                            'required': True,
                            'type': 'text'
                        }
                    }
                },
            )
        else:
            return Response(
                data={
                    'details': _('Registrar not found')
                },
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )

    @action(detail=True, methods=['post'])
    def execute_action(self, request: Request, pk) -> Response:
        del pk  # unused

        domain_action = request.data.get('domain_action', None)
        domain = self.get_object()

        registrar_id = request.data.get('registrar_id', None)
        registrar = Registrar.objects.filter(id=registrar_id).first() if registrar_id else None

        if domain_action and registrar:
            registrar_connector = registrar_connector_manager.get_connector_instance(registrar.connector.name)
            actions = registrar_connector.get_domain_actions(domain=domain)

            if domain_action in actions:
                action_succeeded, message = registrar_connector.execute_domain_action(
                    domain=domain,
                    action=domain_action,
                )
                if action_succeeded:
                    domain.last_registrar = registrar
                    domain.save()
                    return Response(
                        data={
                            'details': _('Action completed successfully'),
                            'action_status': action_succeeded,
                            'action_status_message': message,
                        },
                    )
                else:
                    return Response(
                        data={
                            'details': _('Failed to execute action for domain'),
                            'action_status': action_succeeded,
                            'action_status_message': message,
                        },
                        status=HTTP_422_UNPROCESSABLE_ENTITY,
                    )
            else:
                return Response(
                    data={
                        'details': _('Invalid action for domain'),
                        'action_status': False,
                    },
                    status=HTTP_422_UNPROCESSABLE_ENTITY,
                )
        else:
            return Response(
                data={
                    'details': _('Invalid action or registrar not found'),
                    'action_status': False,
                },
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )

    @action(detail=True, methods=['post'])
    def save_nameservers(self, request: Request, pk) -> Response:
        del pk  # unused
        domain = self.get_object()
        nameservers_data = SaveNameserversSerializer(data=request.data)
        if nameservers_data.is_valid(raise_exception=True):
            with transaction.atomic():
                domain.nameservers.clear()
                for nameserver in [
                    nameservers_data.data.get('nameserver1', None),
                    nameservers_data.data.get('nameserver2', None),
                    nameservers_data.data.get('nameserver3', None),
                    nameservers_data.data.get('nameserver4', None),
                ]:
                    if nameserver:
                        defaults = {'host_name': nameserver}
                        db_nameserver, created = Nameserver.objects.get_or_create(**defaults, defaults=defaults)
                        domain.nameservers.add(db_nameserver)

                domain.save()

                if domain.last_registrar:
                    action_succeeded, message = registrar_connector_manager.get_connector_instance(
                        connector_name=domain.last_registrar.connector.name,
                    ).execute_domain_action(
                        domain=domain, action=DomainActions.update_nameservers
                    )

                    if action_succeeded:
                        return Response(
                            data={
                                'details': message
                            },
                            status=HTTP_200_OK
                        )
                    else:
                        raise APIException(detail=message)
                else:
                    raise APIException(detail=_('No registrar selected'))

            return Response(
                data={
                    'details': _('Nameservers updated successfully')
                },
                status=HTTP_200_OK
            )

    @action(detail=True, methods=['get'])
    def get_whois_fields(self, request: Request, pk) -> Response:
        del request, pk  # unused
        domain = self.get_object()
        whois_fields = []

        if domain.status != DomainStatus.active:
            raise ApiDomainExpectationFailed(
                detail=_('Domain status should be {}').format(DomainStatus.domain_status_map[DomainStatus.active])
            )

        if domain.last_registrar:
            whois_fields = registrar_connector_manager.get_connector_instance(
                connector_name=domain.last_registrar.connector.name,
            ).get_whois_data(domain=domain)

        if len(whois_fields) == 0:
            raise ApiDomainExpectationFailed(
                detail=_('Failed to retrieve whois data for domain')
            )

        whois_fields_definitions = OrderedDict()
        whois_data = {}
        whois_fields_values = []

        for field in whois_fields:
            whois_fields_definitions[field.name] = {
                'required': field.required,
                'optional': not field.required,
                'label': field.label if field.label else field.name,
                'value': field.value,
                'type': 'text',
                'category': '',
            }
            whois_fields_values.append({
                'name': field.name,
                'label': field.label,
                'value': field.value,
            })
            whois_data[field.name] = field.value

        return Response(
            data={
                'whois_fields': whois_fields_definitions,
                'whois_data': {
                    'custom_fields': whois_fields_values
                },
            },
            status=HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def save_whois_data(self, request: Request, pk) -> Response:
        del pk  # unused
        domain = self.get_object()
        whois_fields = []
        connector = registrar_connector_manager.get_connector_instance(
            connector_name=domain.last_registrar.connector.name,
        )

        if domain.last_registrar:
            whois_fields = connector.get_whois_data(domain=domain)

        fields_dict = {field.name: field for field in whois_fields}
        whois_data = request.data.get('whois_data', None)
        if whois_data and 'custom_fields' in whois_data:
            for field in whois_data['custom_fields']:
                name = field['name']
                value = field['value']
                if name in fields_dict:
                    fields_dict[name].value = value

        success, message = connector.set_whois_data(domain=domain, whois_data=whois_fields)

        if success:
            return Response(status=HTTP_200_OK)
        else:
            return Response(
                data={
                    'details': message,
                    'action_status': False,
                },
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )

    def perform_update(self, serializer: Serializer):
        if serializer.is_valid(raise_exception=True):
            previous_instance = self.get_object()  # type: Domain
            registration_period = serializer.validated_data['registration_period']

            if registration_period and registration_period != previous_instance.registration_period:
                # registration period changed, update price cycle
                service = previous_instance.service
                new_cycle = service.product.cycles.filter(
                    cycle_multiplier=registration_period
                ).first()

                if new_cycle:
                    service.cycle = new_cycle
                    service.save()
                else:
                    raise ValidationError(
                        {
                            'registration_period': _(
                                'No price defined for this registration period. Check TLD pricing'
                            )
                        }
                    )

            new_name = serializer.validated_data['name']
            if new_name and new_name != previous_instance.name:
                if not DomainUtils.validate_domain_name(domain_name=new_name):
                    raise ValidationError(
                        {
                            'name': _('Invalid domain name')
                        }
                    )

                try:
                    new_tld_name = DomainUtils.get_tld_name(new_name)
                except ValueError:
                    new_tld_name = None

                if previous_instance.tld.name != new_tld_name:
                    raise ValidationError(
                        {
                            'name': _('New domain name should have the same TLD({})').format(
                                previous_instance.tld.name
                            )
                        }
                    )

            serializer.save()

    def destroy(self, request, *args, **kwargs):
        domain = self.get_object()
        if domain.service and (
                domain.service.client.billing_settings.suspend_instead_of_terminate or
                reseller_suspend_instead_of_terminate(client=domain.service.client)
        ):
            if domain.status in [
                DomainStatus.active,
                DomainStatus.pending_transfer,
                DomainStatus.pending,
                DomainStatus.grace,
                DomainStatus.expired,
            ]:
                with transaction.atomic():
                    domain.status = DomainStatus.cancelled
                    domain.save()
                    domain.service.status = ServiceStatus.suspended
                return Response(
                    {'detail': _('Suspend instead of terminate is enabled for the client, domain canceled.')},
                    status=status.HTTP_202_ACCEPTED
                )

            return Response(
                {'detail': _('Suspend instead of terminate is enabled for the client, domain not deleted.')},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)
