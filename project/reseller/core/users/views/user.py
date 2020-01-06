from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied

from common_admin.core.users.views.user import AdminUserViewSet
from fleio.core.drf import ResellerOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import ForbiddenException
from fleio.core.features import reseller_active_features
from fleio.core.filters import CustomFilter
from fleio.core.models import AppUser
from fleio.core.signals import user_update
from fleio.core.signals import user_update_password
from fleio.core.utils import format_for_log
from fleio.core.utils import get_user_changed_values
from fleio.reseller.utils import filter_queryset_for_user
from fleio.reseller.utils import user_reseller_resources
from reseller.core.signals import reseller_altered_user_data
from reseller.core.signals import reseller_altered_user_password
from reseller.core.signals import reseller_delete_user
from reseller.core.users.serializers.reseller_user_serializer import ResellerUserSerializer
from reseller.core.users.serializers.reseller_user_update_serializer import ResellerUserUpdateSerializer


class ResellerUserViewSet(AdminUserViewSet):
    model = get_user_model()
    permission_classes = (ResellerOnly, )
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

    serializer_map = {
        'update': ResellerUserUpdateSerializer,
    }
    serializer_class = ResellerUserSerializer

    def get_queryset(self):
        return filter_queryset_for_user(super().get_queryset(), self.request.user).all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        if reseller_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        user = serializer.instance
        request_user = self.request.user

        updated_user_fields = get_user_changed_values(user, serializer.validated_data)
        log_text = format_for_log(updated_user_fields)

        password_changed = False
        if 'password' in serializer.validated_data:
            password_changed = True

        reseller_resources = user_reseller_resources(self.request.user)
        # Do not allow editing of users not assigned to reseller
        if user != self.request.user and user.reseller_resources != reseller_resources:
            raise PermissionDenied

        serializer.save()

        if password_changed and updated_user_fields:
            if request_user == user:
                user_update_password.send(
                    sender=__name__, user=request_user, user_id=request_user.pk,
                    username=request_user.username, email=request_user.email, request=self.request,
                )
                user_update.send(
                    sender=__name__, user=request_user, username=request_user.username,
                    user_id=request_user.pk, email=request_user.email, request=self.request, updated_data=log_text,
                )
            else:
                reseller_altered_user_password.send(
                    sender=__name__, user=request_user, user_id=request_user.pk,
                    username=request_user.username, username_changed=user.username,
                    user_changed_id=user.pk, request=self.request,
                )
                reseller_altered_user_data.send(
                    sender=__name__, user=request_user, username=request_user.username,
                    user_id=request_user.pk, username_changed=user.username,
                    user_changed_id=user.pk, request=self.request, updated_data=log_text,
                )
        elif password_changed:
            if request_user == user:
                user_update_password.send(
                    sender=__name__, user=request_user, username=request_user.username,
                    user_id=request_user.pk, email=request_user.email, request=self.request,
                )
            else:
                reseller_altered_user_password.send(
                    sender=__name__, user=request_user, user_id=request_user.pk,
                    username=request_user.username, username_changed=user.username,
                    user_changed_id=user.pk, request=self.request,
                )
        elif updated_user_fields:
            if request_user == user:
                user_update.send(
                    sender=__name__, user=request_user, username=request_user.username,
                    user_id=request_user.pk, email=request_user.email, request=self.request,
                    updated_data=log_text,
                )
            else:
                reseller_altered_user_data.send(
                    sender=__name__, user=request_user, username=request_user.username,
                    user_id=request_user.pk, username_changed=user.username,
                    user_changed_id=user.pk, request=self.request, updated_data=log_text
                )

    def perform_destroy(self, user: AppUser):
        pk = user.id

        if user == self.request.user:
            raise APIBadRequest(_('Cannot delete the user you are logged in with.'))

        # Do not allow editing of users not assigned to reseller
        reseller_resources = user_reseller_resources(self.request.user)
        if user.reseller_resources != reseller_resources:
            raise PermissionDenied

        with transaction.atomic():
            if user.permissions:
                user.permissions.delete()
            user.delete()
            user = self.request.user
            reseller_delete_user.send(
                sender=__name__, user=user, user_id=user.id,
                deleted_user_name=user.username, deleted_user_id=pk,
                username=user.username, request=self.request,
            )
