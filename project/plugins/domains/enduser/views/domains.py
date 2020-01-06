from collections import OrderedDict

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY

from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from fleio.core.drf import EndUserOnly
from fleio.core.filters import CustomFilter

from plugins.domains.enduser.serializers import SaveNameserversSerializer
from plugins.domains.enduser.serializers import DomainSerializer
from plugins.domains.exceptions import ApiDomainExpectationFailed
from plugins.domains.models import Domain
from plugins.domains.models import Nameserver
from plugins.domains.models import Registrar
from plugins.domains.models.domain import DomainStatus
from plugins.domains.registrars_connectors.registrar_connector_base import DomainActions
from plugins.domains.registrars_connectors.registrar_connector_manager import registrar_connector_manager


class DomainsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (EndUserOnly, )
    serializer_class = DomainSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, CustomFilter)
    search_fields = ('name', )
    ordering_fields = ('name', 'created_at',)

    def get_queryset(self):
        return Domain.objects.filter(service__client=self.request.user.clients.first()).all()

    @action(detail=True, methods=['get'])
    def get_info(self, request: Request, pk) -> Response:
        del request, pk  # unused
        domain = self.get_object()
        actions = []

        if domain.status == DomainStatus.active:
            if domain.registrar_locked:
                actions.append({
                    'name': DomainActions.registrar_unlock,
                    'display_name': DomainActions.domain_actions_map[DomainActions.registrar_unlock]
                })
            else:
                actions.append({
                    'name': DomainActions.registrar_lock,
                    'display_name': DomainActions.domain_actions_map[DomainActions.registrar_lock]
                })

            if domain.tld.requires_epp_for_transfer:
                actions.append({
                    'name': DomainActions.get_epp_code,
                    'display_name': DomainActions.domain_actions_map[DomainActions.get_epp_code]
                })

            actions.append({
                'name': DomainActions.renew,
                'display_name': DomainActions.domain_actions_map[DomainActions.renew]
            })

        return Response(
            data={
                'actions': actions
            }
        )

    @action(detail=True, methods=['post'])
    def execute_action(self, request: Request, pk) -> Response:
        del pk  # unused

        domain_action = request.data.get('domain_action', None)
        domain = self.get_object()
        registrar_id = request.data.get('registrar_id', None)
        registrar = Registrar.objects.filter(id=registrar_id).first() if registrar_id else None
        if not registrar:
            registrar = domain.last_registrar

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
                    raise APIException(detail=_('This domain has no registrar associated. Please contact support.'))

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

    @action(detail=False, methods=['get'])
    def get_summary(self, request: Request):
        domains_count = Domain.objects.filter(service__client__in=self.request.user.clients.all()).count()
        return Response(data={
            'domains_count': domains_count
        })
