from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.models import AppUser
from fleio.core.models import Client
from fleio.core.models import TermsOfServiceAgreement
from fleio.core.models import UserGroup
from fleio.reseller.utils import client_reseller_resources
from fleiostaff.core.usergroups.serializers import UserGroupBriefSerializer


class StaffUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    clients = ClientMinSerializer(many=True, required=False, read_only=True)
    user_groups = UserGroupBriefSerializer(many=True, required=False)
    latest_agreed_tos = serializers.SerializerMethodField(read_only=True, required=False)
    reseller_client = serializers.SerializerMethodField(read_only=True, required=False)
    reseller_client_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active',
            'is_reseller', 'clients', 'external_billing_id', 'full_name', 'is_staff', 'is_superuser', 'password',
            'permissions', 'user_groups', 'language', 'email_verified', 'reseller_client', 'latest_agreed_tos',
            'reseller_client_details',
        )
        read_only_fields = ('id', 'date_joined', 'last_login', 'full_name', 'permissions', 'reseller_client_details', )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @staticmethod
    def get_reseller_client(user):
        if user.reseller_resources:
            return user.reseller_resources.service.client.id
        else:
            return None

    @staticmethod
    def get_reseller_client_details(user: AppUser):
        if user.reseller_resources:
            return {
                'name': user.reseller_resources.service.client.name,
                'id': user.reseller_resources.service.client.id,
            }
        else:
            return None

    @staticmethod
    def get_latest_agreed_tos(user):
        tos_agreement = TermsOfServiceAgreement.objects.filter(
            user=user,
            agreed=True
        ).order_by('-terms_of_service__version').first()  # take the latest version
        if not tos_agreement:
            return None
        return dict(
            id=tos_agreement.id,
            version=tos_agreement.terms_of_service.version,
            agreed_at=tos_agreement.agreed_at,
            ip=tos_agreement.ip,
        )

    def create(self, validated_data):
        # user is not associated in any group by default
        if 'user_groups' in validated_data:
            validated_data.pop('user_groups', None)
        if 'language' not in validated_data:
            validated_data['language'] = getattr(settings, 'DEFAULT_USER_LANGUAGE', 'en')
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super(StaffUserSerializer, self).update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class StaffUserUpdateSerializer(StaffUserSerializer):
    user_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=UserGroup.objects.all(),
                                                     required=False)
    reseller_client = serializers.IntegerField(required=False, allow_null=True, default=0)

    class Meta(StaffUserSerializer.Meta):
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def validate(self, attrs):
        if 'reseller_client' in attrs:
            reseller_client_id = attrs.pop('reseller_client', None)
            if reseller_client_id:
                reseller_client = Client.objects.get(id=reseller_client_id)
                attrs['reseller_resources'] = client_reseller_resources(client=reseller_client)
        return attrs
