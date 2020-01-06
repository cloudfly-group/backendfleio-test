from django import forms
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from fleio.core import models
from fleio.core.models.custom_code import CodeInsertionPoints
from fleio.core.models.custom_code import FrontendFileTypes
from fleio.utils.model import dict_to_choices


class PermissionSetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'implicitly_granted')


class PermissionAdminForm(forms.ModelForm):
    name = forms.ChoiceField(choices=models.PermissionNames.get_choices())


def grant_permissions(model_admin, request, queryset):
    del model_admin, request  # unused
    queryset.update(granted=True)


def revoke_permissions(model_admin, request, queryset):
    del model_admin, request  # unused
    queryset.update(granted=False)


grant_permissions.short_description = 'Grant permissions'
revoke_permissions.short_description = 'Revoke permissions'


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'permission_set', 'name', 'granted')
    list_filter = ('permission_set', )
    form = PermissionAdminForm
    actions = [grant_permissions, revoke_permissions]


class ClientAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    list_display = ('__str__', 'get_users', 'currency', 'email', 'country')
    readonly_fields = ('id',)

    @staticmethod
    def get_users(obj):
        return '\n'.join([user.username for user in obj.users.all()])


class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'is_default', 'list_clients')

    @staticmethod
    def list_clients(obj):
        return '\n'.join([client.name for client in obj.clients.all()])


class AuthUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'external_billing_id', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mobile_phone_number', 'language', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_reseller', 'is_staff', 'is_superuser',
                                       'user_groups', 'permissions')}),
        (_('Reseller'), {'fields': ('reseller_resources',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class PluginAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'app_name', 'app_loaded', 'enabled')


class CustomCodeAdminForm(forms.ModelForm):
    insertion_point = forms.ChoiceField(choices=dict_to_choices(CodeInsertionPoints.code_insertion_points_name_map))
    fronted_file_type = forms.ChoiceField(choices=dict_to_choices(FrontendFileTypes.frontend_file_types_map))


class CustomCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'insertion_point', 'frontend_file_type')
    form = CustomCodeAdminForm


class ClientCustomFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', '__str__', 'client')


class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation_type', 'primary_object_id', 'completed', 'status')


class TOSAdmin(admin.ModelAdmin):
    list_display = ('id', 'version')


class TOSAgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'terms_of_service', 'agreed', 'agreed_at', 'ip')


admin.site.register(auth.get_user_model(), AuthUserAdmin)

admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.ClientCustomField, ClientCustomFieldAdmin)
admin.site.register(models.ClientGroup, ClientGroupAdmin)
admin.site.register(models.Currency, admin.ModelAdmin)

admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.PermissionSet, PermissionSetAdmin)
admin.site.register(models.Plugin, PluginAdmin)

admin.site.register(models.UserToClient, admin.ModelAdmin)
admin.site.register(models.UserGroup)


admin.site.register(models.CustomCode, CustomCodeAdmin)

admin.site.register(models.AppStatus, admin.ModelAdmin)

admin.site.register(models.SecondFactorAuthType, admin.ModelAdmin)

admin.site.register(models.SecondFactorAuthMethod, admin.ModelAdmin)

admin.site.register(models.Operation, OperationAdmin)

admin.site.register(models.TermsOfService, TOSAdmin)

admin.site.register(models.TermsOfServiceAgreement, TOSAgreementAdmin)
