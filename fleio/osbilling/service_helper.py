from django.db import transaction

from .models import PricingPlan
from .models import ServiceDynamicUsage
from fleio.billing.models import Service


class ServiceHelper:
    @staticmethod
    def init_service_dynamic_usage(service: Service):
        service_dynamic_usage = ServiceDynamicUsage.objects.filter(
            service=service, reseller_service=None
        ).first()

        if service_dynamic_usage is None:
            ServiceDynamicUsage.objects.create(
                service=service,
                plan=PricingPlan.objects.get_default_or_any_or_create(
                    currency=service.client.currency,
                    # if reseller_resources is None then staff default billing plan will be used
                    reseller_resources=service.client.reseller_resources,
                )
            )

        ServiceHelper.init_reseller_service_dynamic_usage(service)

    @staticmethod
    def init_reseller_service_dynamic_usage(service: Service):
        if service.client.reseller_resources:
            # client is assigned to a reseller, init reseller service dynamic usage too
            reseller_service_dynamic_usage = ServiceDynamicUsage.objects.filter(
                service=None, reseller_service=service
            ).first()
            if reseller_service_dynamic_usage is None:
                plan = service.client.reseller_resources.plan
                if not plan:
                    plan = PricingPlan.objects.get_default_or_any_or_create(
                        # reseller is billed using staff billing plan
                        currency=service.client.currency,
                    )
                ServiceDynamicUsage.objects.create(
                    reseller_service=service,
                    service=None,
                    plan=plan,
                )

    @staticmethod
    def set_new_reseller(service: Service):
        with transaction.atomic():
            reseller_service_dynamic_usage = ServiceDynamicUsage.objects.filter(
                service=None, reseller_service=service
            ).first()

            if not reseller_service_dynamic_usage:
                ServiceHelper.init_reseller_service_dynamic_usage(service)
            else:
                reseller_service_dynamic_usage.plan = PricingPlan.objects.get_default_or_any_or_create(
                    # reseller is billed using staff billing plan
                    currency=service.client.currency,
                )
                reseller_service_dynamic_usage.save()

            service.service_dynamic_usage.plan = PricingPlan.objects.get_default_or_any_or_create(
                currency=service.client.currency,
                # if reseller_resources is None then staff default billing plan will be used
                reseller_resources=service.client.reseller_resources,
            )

            service.service_dynamic_usage.save()

    @staticmethod
    def clear_reseller(service):
        with transaction.atomic():
            reseller_service_dynamic_usage = ServiceDynamicUsage.objects.filter(
                service=None, reseller_service=service
            ).first()

            # TODO: see if this is ok and if this affects revenue reports
            if reseller_service_dynamic_usage:
                reseller_service_dynamic_usage.delete()

            service.service_dynamic_usage.plan = PricingPlan.objects.get_default_or_any_or_create(
                currency=service.client.currency,
                # if reseller_resources is None then staff default billing plan will be used
                reseller_resources=service.client.reseller_resources,
            )

            service.service_dynamic_usage.save()
