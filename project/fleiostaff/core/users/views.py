from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from common_admin.core.users.views.user import AdminUserViewSet
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import ForbiddenException
from fleio.core.features import staff_active_features
from fleio.core.filters import CustomFilter
from fleio.core.models import AppUser
from fleio.core.models import Permission
from fleio.core.models import PermissionNames
from fleio.core.models import PermissionSet
from fleio.core.models import UserGroup
from fleio.core.permissions import permissions
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.signals import user_update
from fleio.core.signals import user_update_password
from fleio.core.utils import format_for_log
from fleio.core.utils import get_user_changed_values
from fleiostaff.core.permissions.serializers import PermissionUpdateSerializer
from fleiostaff.core.signals import staff_altered_user_data
from fleiostaff.core.signals import staff_altered_user_password
from fleiostaff.core.signals import staff_delete_user
from .serializers import StaffUserSerializer
from .serializers import StaffUserUpdateSerializer


class UserViewSet(AdminUserViewSet):
    model = get_user_model()
    permission_classes = (StaffOnly, )
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    ordering_fields = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active')
    filter_fields = (
        'username',
        'email',
        'id',
        'first_name',
        'last_name',
        'external_billing_id',
        'is_reseller',
        'is_staff',
        'is_superuser'
    )
    search_fields = ('first_name', 'last_name', 'id', 'email', 'username', 'user_groups__name')

    serializer_map = {'update': StaffUserUpdateSerializer,
                      'generate_permission_set': PermissionUpdateSerializer}
    serializer_class = StaffUserSerializer

    @action(detail=True, methods=['post'])
    def token(self, request, pk):
        del request, pk  # unused
        user = self.get_object()
        if not user.is_active:
            raise ForbiddenException(detail=_('User account is inactive'))
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    @action(detail=True, methods=['delete'])
    def delete_token(self, request, pk):
        del request, pk  # unused
        user = self.get_object()

        try:
            Token.objects.get(user=user).delete()
        except Token.DoesNotExist:
            return Response(
                {'detail': _('No token associated with user: {0} ({1})').format(user.username, user.id)}
            )
        else:
            return Response(
                {'detail': _('Token associated with user: {0} ({1}) deleted.'.format(user.username, user.id))}
            )

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        new_user_is_superuser = serializer.validated_data.get('is_superuser')
        if new_user_is_superuser and staff_active_features.is_enabled('demo'):
            # don't allow creation of superusers in demo mode
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))
        # Don't allow users to create super users
        if new_user_is_superuser is True and self.request.user.is_superuser is False:
            raise PermissionDenied
        serializer.save()

    def perform_update(self, serializer):
        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        user = serializer.instance
        request_user = self.request.user

        updated_user_fields = get_user_changed_values(user, serializer.validated_data)
        log_text = format_for_log(updated_user_fields)

        password_changed = False
        if 'password' in serializer.validated_data:
            password_changed = True

        # Don't allow users to edit super user
        if user.is_superuser:
            if request_user.is_superuser is False:
                raise PermissionDenied

        # Change superuser status only if the user who makes the request is also a superuser
        if 'is_superuser' in serializer.validated_data:
            if request_user.is_superuser is False:
                serializer.validated_data.pop('is_superuser', None)
            else:
                # if the instance user gets marked as superuser also mark it as staff
                if serializer.validated_data['is_superuser'] is True:
                    serializer.validated_data['is_staff'] = True

        # Don't allow superuser to remove it's own superuser status
        if request_user == user and request_user.is_superuser is True:
            if 'is_superuser' in serializer.validated_data:
                if serializer.validated_data['is_superuser'] is False:
                    raise APIBadRequest(detail=_('Cannot remove own superuser status'))

        # Don't allow updating a regular user to staff if user has clients
        if serializer.validated_data.get('is_staff', False) and not user.is_staff:
            if user.clients.count() > 0:
                raise APIBadRequest(
                    detail=_('Cannot have a staff user with clients associated. Dissociate all clients and try again.'),
                )

        serializer.save()

        if password_changed and updated_user_fields:
            if request_user == user:
                user_update_password.send(sender=__name__, user=request_user, user_id=request_user.pk,
                                          username=request_user.username, email=request_user.email,
                                          request=self.request)
                user_update.send(sender=__name__, user=request_user, username=request_user.username,
                                 user_id=request_user.pk, email=request_user.email, request=self.request,
                                 updated_data=log_text)
            else:
                staff_altered_user_password.send(sender=__name__, user=request_user, user_id=request_user.pk,
                                                 username=request_user.username, username_changed=user.username,
                                                 user_changed_id=user.pk, request=self.request)
                staff_altered_user_data.send(sender=__name__, user=request_user, username=request_user.username,
                                             user_id=request_user.pk, username_changed=user.username,
                                             user_changed_id=user.pk, request=self.request, updated_data=log_text)
        elif password_changed:
            if request_user == user:
                user_update_password.send(sender=__name__, user=request_user, username=request_user.username,
                                          user_id=request_user.pk, email=request_user.email, request=self.request)
            else:
                staff_altered_user_password.send(sender=__name__, user=request_user, user_id=request_user.pk,
                                                 username=request_user.username, username_changed=user.username,
                                                 user_changed_id=user.pk, request=self.request)
        elif updated_user_fields:
            if request_user == user:
                user_update.send(sender=__name__, user=request_user, username=request_user.username,
                                 user_id=request_user.pk, email=request_user.email, request=self.request,
                                 updated_data=log_text)
            else:
                staff_altered_user_data.send(sender=__name__, user=request_user, username=request_user.username,
                                             user_id=request_user.pk, username_changed=user.username,
                                             user_changed_id=user.pk, request=self.request, updated_data=log_text)

    def perform_destroy(self, instance: AppUser):
        if (instance.is_superuser or instance.username == 'demo') and staff_active_features.is_enabled('demo'):
            # don't allow deletion of superuser or enduser demo account in demo mode
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))
        if instance.is_superuser:
            if self.request.user.username == instance.username or self.request.user.is_superuser is False:
                raise PermissionDenied
        pk = instance.id
        if instance.username == self.request.user.username:
            raise APIBadRequest(_('Cannot delete the user you are logged in with.'))
        with transaction.atomic():
            if instance.permissions:
                instance.permissions.delete()
            instance.delete()
            user = self.request.user
            staff_delete_user.send(sender=__name__, user=user, user_id=user.id,
                                   deleted_user_name=instance.username, deleted_user_id=pk,
                                   username=user.username, request=self.request)

    @action(detail=True, methods=['post'])
    def generate_permission_set(self, request, pk):
        del pk  # unused
        user = self.get_object()
        if user.permissions is None:
            with transaction.atomic():
                permission_set_name = '{}{}'.format(user.username, user.id)
                granted = getattr(settings, 'GRANT_ALL_PERMISSIONS_IMPLICITLY', False)
                permission_set = PermissionSet.objects.create(name=permission_set_name, implicitly_granted=granted)
                user.permissions = permission_set
                user.save()
                # after the permission set was created and assigned to the user update it with the received data
                to_be_updated = Permission.objects.filter(permission_set=permission_set)
                update_serializer = PermissionUpdateSerializer(
                    to_be_updated,
                    data=request.data['objects'],
                    many=True,
                    context={
                        # get the permission set that needs to be updated
                        "permissions_set": permission_set.id
                    }
                )
                if update_serializer.is_valid():
                    update_serializer.save()
                    implicitly_granted = getattr(settings, 'GRANT_ALL_PERMISSIONS_IMPLICITLY', False)
                    permission_set.implicitly_granted = request.data.get('implicitly_granted', implicitly_granted)
                    permission_set.save()
                    return Response({
                        'detail': _('Permission set {} for user {} created and updated successfully.'.format(
                            permission_set.name,
                            user.username
                        )),
                        'permissions_set': user.permissions.id
                    })
                else:
                    raise APIBadRequest(detail=_('Invalid data provided'))
        else:
            raise APIBadRequest(detail=_('User already has a permission set assigned'))

    @action(detail=True, methods=['get'])
    def fetch_effective_permissions(self, request, pk):
        del request, pk  # unused
        user = self.get_object()
        if user.permissions is not None:
            permissions_cache.cache_user_permissions(user)
            perms = permissions_cache.get_user_permissions(user)
            return Response({
                'detail': _('Effective permissions fetched successfully'),
                'permissions': perms.permissions
            })
        else:
            permissions_cache.cache_user_permissions(user)
            perms = permissions_cache.get_user_permissions(user)
            return Response({
                'detail': _('Effective permissions fetched successfully'),
                'permissions': perms.get_permission_dict()
            })

    @action(detail=True, methods=['get'])
    def list_permissions(self, request, pk):
        del request, pk  # unused
        user = self.get_object()
        names_map = PermissionNames.permissions_map
        description_map = PermissionNames.permissions_description_map
        if user.permissions is not None:
            user_permissions = permissions.Permissions(permission_set=user.permissions)
        else:
            permissions_cache.cache_user_permissions(user)
            user_permissions = permissions_cache.get_user_permissions(user)
        perms = user_permissions.get_permission_dict().items()
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
                "implicitly_granted": user_permissions.implicitly_granted,
            }
        )

    @action(detail=False, methods=['get'])
    def get_available_users_for_group(self, request):
        group_id = request.query_params.get('group')
        is_staff = request.query_params.get('is_staff', False)
        search = request.query_params.get('search')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter users against it'))
        try:
            group = UserGroup.objects.get(id=group_id)
        except UserGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))
        queryset = AppUser.objects.all()
        if is_staff:
            queryset = queryset.filter(is_staff=True)
        queryset = queryset.exclude(user_groups=group)
        if search:
            queryset = queryset.filter(username__startswith=search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = StaffUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = StaffUserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_users_in_group(self, request):
        group_id = request.query_params.get('group_id')
        if not group_id:
            raise APIBadRequest(_('Missing group id to filter users against it'))
        try:
            group = UserGroup.objects.get(id=group_id)
        except UserGroup.DoesNotExist:
            raise APIBadRequest(_('No group to filter against'))
        queryset = AppUser.objects.filter(user_groups__in=[group])
        try:
            page = self.paginate_queryset(queryset)
        except Exception as e:
            del e  # unused
            raise APIBadRequest(_('Invalid page'))
        if page is not None:
            serializer = StaffUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = StaffUserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_user_to_group(self, request, pk):
        del pk  # unused
        user = self.get_object()  # type: AppUser
        group_id = request.query_params.get('group_id', None)
        if not group_id:
            raise APIBadRequest(_('Missing group id'))
        try:
            group = UserGroup.objects.get(id=group_id)
        except UserGroup.DoesNotExist:
            raise APIBadRequest(_('No group with the provided id found'))
        try:
            user.user_groups.add(group)
        except Exception as e:
            raise e
        else:
            return Response({'detail': _('Successfully added user to group')})

    @action(detail=True, methods=['POST'])
    def remove_user_from_group(self, request, pk):
        del pk  # unused
        user = self.get_object()  # type: AppUser
        group_id = request.query_params.get('group_id', None)
        if not group_id:
            raise APIBadRequest(_('Missing group id'))
        try:
            group = UserGroup.objects.get(id=group_id)
        except UserGroup.DoesNotExist:
            raise APIBadRequest(_('No group with the provided id found'))
        try:
            user.user_groups.remove(group)
        except Exception as e:
            raise e
        else:
            return Response({'detail': _('Successfully added user to group')})
