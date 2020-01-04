import logging
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from keystoneauth1.exceptions import ClientException

from common_admin.openstack.users.views.user import AdminOpenStackUsersViewSet
from fleio.core.drf import CustomPermissions, ResellerOnly

from fleio.openstack.models import Project
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.openstack.users.serializers import UserSerializer


LOG = logging.getLogger(__name__)


class ResellerOpenStackUsersViewSet(AdminOpenStackUsersViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)

    def projects_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return Project.objects.filter(service__client__reseller_resources=reseller_resources)

    def list(self, request):
        try:
            os_users = self.get_api_users()
            serializer = UserSerializer(data=os_users, many=True)
            serializer.is_valid(raise_exception=True)
        except ClientException as e:
            LOG.error('OpenStack list users failed, reason: {0}'.format(e))
            raise ValidationError({'detail': _('Unable to list users. Please contact support for more info')})
        else:
            return Response({
                'objects': serializer.data,
                'count': len(os_users),
                'totalCount': len(os_users),
            }, status=HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        return self.edit_user_data(request=request)
