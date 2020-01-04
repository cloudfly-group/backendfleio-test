import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from keystoneauth1.exceptions.connection import ConnectFailure
from keystoneauth1.exceptions.http import Conflict
from keystoneauth1.exceptions.http import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fleio.billing.models import Product
from fleio.billing.products.serializers import ProductSerializer
from fleio.billing.services.serializers import ServiceBriefSerializer
from fleio.billing.settings import ProductType
from fleio.conf.exceptions import ConfigException
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import ForbiddenException, ObjectNotFound, ServiceUnavailable
from fleio.core.models import Client
from fleio.openstack.api.identity import IdentityAdminApi, RoleDoesNotExist
from fleio.openstack.models import Project as ProjectModel
from fleio.openstack.project import Project as OpenstackProject
from fleio.openstack.settings import plugin_settings
from fleiostaff.core.clients.serializers import StaffClientSerializer
from .serializers import CreateServiceSerializer, ProjectSerializer

LOG = logging.getLogger(__name__)


class OpenstackClientsViewSet(ModelViewSet):
    permission_classes = (StaffOnly,)
    model = Client
    serializer_class = StaffClientSerializer
    queryset = Client.objects.all()

    @action(detail=True, methods=['get'])
    def openstack_services(self, request, pk):
        del request, pk  # unused
        client = self.get_object()
        services = client.services.select_related('openstack_project').filter(
            product__product_type=ProductType.openstack,
            openstack_project__isnull=False
        )

        projects = []

        for service in services:
            try:
                project = service.openstack_project
            except ObjectDoesNotExist:
                project = None

            if project is not None:
                try:
                    if OpenstackProject.with_admin_session(project.project_id) is None:
                        project = None
                except Exception as e:
                    LOG.exception(e)
                    project = None

            if project is not None:
                projects.append(project)

        serialized_services = ServiceBriefSerializer(many=True).to_representation(services)
        serialized_projects = ProjectSerializer(many=True).to_representation(projects)

        return Response({'services': serialized_services,
                         'projects': {project['service']: project for project in serialized_projects}})

    @action(detail=True, methods=['get'])
    def new_service_data(self, request, pk):
        del request, pk  # unused
        products = Product.objects.filter(product_type=ProductType.openstack)

        return Response({
            'products': ProductSerializer(products, many=True).data,
        })

    @action(detail=True, methods=['post'])
    def create_openstack_service(self, request, pk):
        del pk  # unused

        # TODO - #1019: implement proper creation of service here
        serializer = CreateServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = self.get_object()

        if client.first_project is not None and client.first_project.deleted is False:
            raise ForbiddenException({'detail': _('Client already has a project')})

        project_id = serializer.validated_data.get('project_id', 'none')

        if Client.objects.filter(services__openstack_project__project_id=project_id):
            raise ForbiddenException({'detail': _('Project already associated with a client')})

        openstack_product = Product.objects.get(id=serializer.validated_data['product_id'])
        openstack_product_cycle = openstack_product.cycles.filter(id=serializer.validated_data['product_cycle_id'])[0]
        service_external_id = serializer.validated_data.get('service_external_id', None)

        with transaction.atomic():
            if serializer.validated_data['create_new_project']:
                try:
                    ProjectModel.objects.create_project(
                        client=client,
                        openstack_product=openstack_product,
                        openstack_product_cycle=openstack_product_cycle,
                        service_external_id=service_external_id,
                    )
                except Conflict:
                    return Response(status=409, data={'detail': _('A project already exists for this client')})
                except RoleDoesNotExist:
                    # TODO: going to the exact settings page and field isn't implemented yet in frontend
                    # on implementation in frontend change section and configuration_id if necessary
                    # (Issue: https://git.fleio.org/fleio/fleio/issues/1922)
                    if plugin_settings.default_role:
                        error_message = _('Role "{}" does not exist in OpenStack. Set an existing role as default '
                                          'role.').format(plugin_settings.default_role)
                    else:
                        error_message = _('OpenStack role was not set in OpenStack settings -> defaults tab. '
                                          'Set an existing role as default role.')
                    raise ConfigException(
                        message=error_message,
                        section='openstack_plugin_defaults',
                        configuration_id='default_role'
                    )
            else:
                try:
                    project = IdentityAdminApi(request_session=request.session).client.projects.get(project_id)
                except NotFound:
                    raise ObjectNotFound({'detail': _('Project not found')})
                except ConnectFailure:
                    raise ServiceUnavailable({'detail': _('Could not connect to openstack')})

                with transaction.atomic():
                    try:
                        ProjectModel.objects.create_project(
                            client=client,
                            openstack_product=openstack_product,
                            openstack_product_cycle=openstack_product_cycle,
                            service_external_id=service_external_id,
                            project_id=project.id,
                            project_domain_id=project.domain_id,
                            disabled=not project.enabled,
                            extras={
                                'name': project.name,
                                'description': project.description,
                                'is_domain': project.is_domain
                            }).save()
                    except RoleDoesNotExist:
                        # TODO: going to the exact settings page and field isn't implemented yet in frontend
                        # on implementation in frontend change section and configuration_id if necessary
                        # (Issue: https://git.fleio.org/fleio/fleio/issues/1922)
                        if plugin_settings.default_role:
                            error_message = _('Role "{}" does not exist in OpenStack. Set an existing role as default '
                                              'role.').format(plugin_settings.default_role)
                        else:
                            error_message = _('OpenStack role was not set in OpenStack settings -> defaults tab. '
                                              'Set an existing role as default role.')
                        raise ConfigException(
                            message=error_message,
                            section='openstack_plugin_defaults',
                            configuration_id='default_role'
                        )

        return Response({'detail': _('Ok')})
