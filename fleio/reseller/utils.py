from typing import Optional

from fleio.core.models import AppUser
from fleio.core.models import Client
from fleio.reseller.models import ResellerResources


def user_reseller_resources(user: AppUser) -> ResellerResources:
    return ResellerResources.objects.for_user(user=user).first()


def client_reseller_resources(client: Client) -> ResellerResources:
    return ResellerResources.objects.for_client(client=client).first()


def filter_queryset_for_user(queryset, user: AppUser):
    return queryset.filter(reseller_resources=user_reseller_resources(user=user))


def filter_queryset_for_client(queryset, client: Client):
    return queryset.filter(reseller_resources=client_reseller_resources(client=client))


def reseller_suspend_instead_of_terminate(client: Optional[Client] = None) -> bool:
    reseller_resources = client.reseller_resources if client else None
    if reseller_resources:
        return reseller_resources.service.client.billing_settings.suspend_instead_of_terminate

    return False
