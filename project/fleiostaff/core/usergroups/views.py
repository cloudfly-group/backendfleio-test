from django.conf import settings

from rest_framework import viewsets
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.models import AppUser, PermissionSet, UserGroup
from fleio.core.filters import CustomFilter
from fleio.core.permissions import permissions
from fleio.core.models import Permission, PermissionNames

from fleiostaff.core.usergroups.serializers import UserGroupDetailSerializer, UserGroupSerializer
from fleiostaff.core.permissions.serializers import PermissionUpdateSerializer


@log_staff_activity(category_name='core', object_name=_('user group'))
class UserGroupViewset(viewsets.ModelViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = UserGroupSerializer
    queryset = UserGroup.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    ordering_fields = ('name', 'id', 'created_at',)
    filter_fields = ('name',)
    search_fields = ('name',)
    model = UserGroup

    serializer_map = {'generate_permission_set': PermissionUpdateSerializer,
                      'retrieve': UserGroupDetailSerializer}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, UserGroupSerializer)

    def perform_destroy(self, instance: UserGroup):
        with transaction.atomic():
            if instance.permissions:
                instance.permissions.delete()
            instance.delete()

    @action(detail=True, methods=['get'])
    def list_permissions(self, request, pk):
        del request, pk  # unused
        usergroup = self.get_object()
        names_map = PermissionNames.permissions_map
        description_map = PermissionNames.permissions_description_map
        if usergroup.permissions is not None:
            group_permissions = permissions.Permissions(permission_set=usergroup.permissions)
        else:
            if getattr(settings, 'GRANT_ALL_PERMISSIONS_IMPLICITLY', False) is True:
                group_permissions = permissions.ALL_PERMISSIONS
            else:
                group_permissions = permissions.NO_PERMISSIONS
        perms = group_permissions.get_permission_dict().items()
        permissions_list = []
        for key, value in perms:
            permission = {
                'name': key,
                'display_name': names_map[key],
                'granted': value
            }
            if key in description_map:
                permission['description'] = description_map[key]
            permissions_list.append(permission)
        # add info about permissions' categories
        permissions_list.sort(key=lambda tup: tup['name'])
        permissions_list[0]['category'] = permissions_list[0]['name'].split('.')[0]
        for index, perm in enumerate(permissions_list):
            if index < len(permissions_list) - 1:
                next_category_name = permissions_list[index + 1]['name'].split('.')[0]
                category_name = perm['name'].split('.')[0]
                if next_category_name.startswith(category_name):
                    perm['display_data'] = {
                        'last_in_category': False,
                        'category': category_name
                    }
                else:
                    perm['display_data'] = {
                        'last_in_category': True,
                        'category': category_name,
                        'next_category': next_category_name
                    }
        return Response(
            {
                "objects": permissions_list,
                "implicitly_granted": group_permissions.implicitly_granted,
            }
        )

    @action(detail=True, methods=['post'])
    def generate_permission_set(self, request, pk):
        del pk  # unused
        usergroup = self.get_object()
        if usergroup.permissions is None:
            with transaction.atomic():
                permission_set_name = '{}{}'.format(usergroup.name, usergroup.id)
                granted = getattr(settings, 'GRANT_ALL_PERMISSIONS_IMPLICITLY', False)
                permission_set = PermissionSet.objects.create(name=permission_set_name, implicitly_granted=granted)
                usergroup.permissions = permission_set
                usergroup.save()
                # after the permission set was created and assigned to the user update it with the received data
                to_be_updated = Permission.objects.filter(permission_set=permission_set)
                update_serializer = PermissionUpdateSerializer(
                    to_be_updated,
                    data=request.data['objects'],
                    many=True,
                    context={
                        # send the permission set that needs to be updated
                        "permissions_set": permission_set.id
                    }
                )
                if update_serializer.is_valid():
                    update_serializer.save()
                    implicitly_granted = getattr(settings, 'GRANT_ALL_PERMISSIONS_IMPLICITLY', False)
                    permission_set.implicitly_granted = request.data.get('implicitly_granted', implicitly_granted)
                    permission_set.save()
                    return Response({
                        'detail': _('Permission set {} for user group {} created and updated successfully.'.format(
                            permission_set.name,
                            usergroup.name
                        )),
                        'permissions_set': usergroup.permissions.id
                    })
                else:
                    raise APIBadRequest(detail=_('Invalid data provided'))
        else:
            raise APIBadRequest(detail=_('User group already has a permission set assigned'))

    @action(detail=False, methods=['GET'])
    def get_groups_available_for_user(self, request):
        """
        Gets user groups where a given user is not associated with them
        :param request:
        :return:
        """
        user_id = request.query_params.get('user_id', None)
        search = request.query_params.get('search', None)
        if not user_id:
            raise APIBadRequest(_('Missing user id to get groups for.'))
        try:
            user = AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            raise APIBadRequest(_('User with provided id not found.'))
        if search:
            qs = UserGroup.objects.filter(name=search)
        else:
            qs = UserGroup.objects.all()
        qs = qs.exclude(users__in=[user])
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = UserGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserGroupSerializer(qs, many=True)
        return Response(serializer.data)
