from typing import List

import celery
from django.conf import settings
from django.db import transaction
from django.db.models import CharField
from django.db.models import F
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Value
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.billing.client_operations import ClientOperations
from fleio.billing.models import Journal
from fleio.billing.models.journal_sources import JournalSources
from fleio.billing.services import tasks as service_tasks
from fleio.core.custom_fields.client_customfield_definition import ClientCustomFieldDefinition
from fleio.core.drf import SuperUserOnly
from fleio.core.models import Client
from fleio.core.models import ClientGroup
from fleio.core.models import ClientStatus
from fleio.core.models import Configuration
from fleio.core.models import Currency
from fleio.core.models import get_default_currency
from fleio.core.serializers import UserMinSerializer
from fleio.core.utils import get_countries
from fleio.openstack.models import Project
from fleiostaff.core.utils import annotate_clients_queryset
from fleiostaff.openstack.core.serializers import OpenstackProjectBriefSerializer


class AdminClientViewSet(ModelViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_map = {}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @staticmethod
    def get_email_variables() -> List[str]:
        return [
            'name', 'first_name', 'last_name', 'company', 'city', 'country', 'state',
            'currency', 'phone', 'country_name', 'long_name', 'fax', 'address1', 'address2', 'email',
            'zip_code', 'vat_id', 'uptodate_credit', 'status', 'outofcredit_datetime',
        ]

    @staticmethod
    def annotate_configuration_and_group(list_queryset):
        if Configuration.objects.count() > 1:
            list_queryset = list_queryset.annotate(configuration_name=F('configuration__name'))
        else:
            list_queryset = list_queryset.annotate(configuration_name=Value('', CharField()))
        if ClientGroup.objects.count() > 1:
            groups = ClientGroup.objects.filter(clients=OuterRef('pk'))
            list_queryset = list_queryset.annotate(group_name=Subquery(groups.values('name')[:1]))
        else:
            list_queryset = list_queryset.annotate(group_name=Value('', CharField()))
        list_queryset = annotate_clients_queryset(list_queryset)
        return list_queryset

    def get_queryset(self):
        if self.action == 'list':
            list_queryset = Client.objects
            list_queryset = self.annotate_configuration_and_group(list_queryset)

            return list_queryset.all()

        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        del request  # unused
        default_currency = get_default_currency()  # type: Currency
        create_options = {
            'countries': get_countries(),
            'currencies': [currency.code for currency in Currency.objects.all()],
            'default_currency': default_currency.code if default_currency else None,
            'custom_fields': ClientCustomFieldDefinition().definition,
            'max_email_attachment_size': settings.MAX_EMAIL_ATTACHMENT_SIZE,
            'email_variables': ['{}{}{}'.format('{{ ', name, ' }}') for name in self.get_email_variables()],
        }
        return Response(create_options)

    @action(detail=True, methods=['post'])
    def suspend(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        activity_helper.add_current_activity_params(client_name=client.name)

        if client.status == ClientStatus.suspended:
            return Response({'detail': _('Client already suspended')})

        suspend_service_tasks = list()
        for service in client.services.active():
            # TODO - #1015: seems like reason is not sent to this method, passing empty reason
            suspend_service_tasks.append(service_tasks.suspend_service.s(service.id, ''))

        celery.group(suspend_service_tasks).apply_async()

        client.status = ClientStatus.suspended
        client.save()

        return Response({'detail': _('Suspend scheduled')})

    @action(detail=True, methods=['post'])
    def resume(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        activity_helper.add_current_activity_params(client_name=client.name)

        if client.status == ClientStatus.active:
            return Response({'detail': _('Client is not suspended')})

        resume_service_tasks = list()
        for service in client.services.suspended():
            resume_service_tasks.append(service_tasks.resume_service.s(service.id))

        celery.group(resume_service_tasks).apply_async()

        client.status = ClientStatus.active
        client.save()

        return Response({'detail': _('Resume scheduled')})

    @action(detail=True, methods=['post'])
    def change_credit(self, request, pk):
        del pk  # unused
        client = self.get_object()
        sr = self.get_serializer(data=request.data, instance=client)
        sr.is_valid(raise_exception=True)
        amount = sr.validated_data['amount']
        currency = sr.validated_data.get('currency', client.currency)
        exchange_rate = sr.validated_data.get('exchange_rate', 1)
        source_amount = sr.validated_data.get('source_amount', amount)
        source_currency = sr.validated_data.get('source_currency', client.currency)
        external_source = sr.validated_data['external_source']
        with transaction.atomic():
            client_operations = ClientOperations(client=client)
            if sr.validated_data['add_credit']:
                new_balance = client.add_credit(amount, currency)
                source = JournalSources.external if external_source else JournalSources.staff
                destination = JournalSources.credit

                client_operations.update_usage(skip_collecting=True)
                client_operations.evaluate_and_resume_if_enough_credit()
            else:
                new_balance = client.withdraw_credit(amount, currency)
                source = JournalSources.credit
                destination = JournalSources.external if external_source else JournalSources.staff
                client_operations.update_usage(skip_collecting=True)
                client_operations.evaluate_and_suspend_if_overdue()

            credit = client.credits.get(currency=currency)
            Journal.objects.create(client_credit=credit,
                                   transaction=None,
                                   source_currency=source_currency,
                                   destination_currency=currency,
                                   source=source,
                                   destination=destination,
                                   source_amount=source_amount,
                                   destination_amount=amount,
                                   exchange_rate=exchange_rate,
                                   user=request.user)

        return Response({'credit_balance': new_balance, 'client': client.id}, status=HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_users(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        return Response({'users': UserMinSerializer(instance=client.users, many=True).data})

    @action(detail=True, methods=['get'])
    def get_configuration(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        return Response(
            {
                'id': client.active_configuration.id,
                'name': client.active_configuration.name
            }
        )

    @action(detail=True, methods=['get'])
    def get_os_projects_for_os_service_creation(self, request, pk):
        # TODO: move this to openstack projects viewset
        del pk  # unused
        """Allows searching for projects without related service"""
        search = request.query_params.get('search', None)
        if search:
            filtering_params = Q(service=None) & (Q(name__contains=search) | Q(project_id__startswith=search))
            projects_qs = Project.objects.filter(filtering_params)
        else:
            projects_qs = Project.objects.filter(service=None)

        projects_qs = projects_qs.order_by('-created_at')
        page = self.paginate_queryset(projects_qs)
        if page is not None:
            serializer = OpenstackProjectBriefSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        projects = OpenstackProjectBriefSerializer(instance=projects_qs, many=True).data
        return Response({
            'objects': projects
        })
