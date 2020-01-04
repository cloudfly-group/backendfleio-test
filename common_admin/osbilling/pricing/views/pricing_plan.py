from django.utils.translation import ugettext_lazy as _

from types import SimpleNamespace

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common_admin.osbilling.pricing.serializers.pricing_plan import AdminPricingPlanCreateOptionsSerializer
from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.models import Currency
from fleio.osbilling.models import PricingPlan
from fleio.osbilling.models import ServiceDynamicUsage


class AdminPricingPlanViewSet(ModelViewSet):
    permission_classes = (SuperUserOnly,)
    ordering = ['id']
    filter_fields = ('id', 'is_default', )
    ordering_fields = ('name', 'currency')
    search_fields = ('name', 'currency__code')
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    queryset = PricingPlan.objects.all()
    serializer_map = {}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def destroy(self, request, *args, **kwargs):
        plan = self.get_object()
        name = plan.name
        DeleteSerializer = self.get_serializer_class()
        serializer = DeleteSerializer(data=request.GET, plan=plan)
        serializer.is_valid(raise_exception=True)
        plan_to_migrate = serializer.validated_data['plan_to_migrate']  # type: PricingPlan
        service_dynamic_usages = ServiceDynamicUsage.objects.filter(plan=plan)
        services_count = service_dynamic_usages.count()
        for service_dynamic_usage in service_dynamic_usages:
            service_dynamic_usage.plan = plan_to_migrate
            service_dynamic_usage.save()

        if plan.is_default and plan_to_migrate.reseller_resources == plan.reseller_resources:
            plan_to_migrate.is_default = True
            plan_to_migrate.save()

        plan.delete()
        return Response({
            'detail': _(
                'Plan {old_plan} deleted and {services_count} services migrated to plan {new_plan}'
            ).format(
                old_plan=name,
                services_count=services_count,
                new_plan=plan_to_migrate.name
            )
        })

    def update(self, request, *args, **kwargs):
        UpdateSerializer = self.get_serializer_class()
        serializer = UpdateSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        plan = self.get_object()
        default_plans = self.get_queryset().filter(is_default=True, reseller_resources=plan.reseller_resources)
        if not plan.is_default and serializer.validated_data.get('is_default'):
            for df_plan in default_plans:
                df_plan.is_default = False
                df_plan.save()
        elif not default_plans.exclude(id=plan.id) and not serializer.validated_data.get('is_default'):
            other_default = serializer.validated_data.get('other_default')
            if not other_default:
                raise APIBadRequest(_('There must be a default billing plan'))
            else:
                other_default.is_default = True
                other_default.save()
        plan.is_default = serializer.validated_data.get('is_default')
        plan.name = serializer.validated_data['name']
        plan.currency = serializer.validated_data['currency']
        plan.save()
        return Response({'plan': self.serializer_class(plan).data})

    @action(detail=False, methods=['GET'])
    def create_options(self, request):
        del request  # unused

        create_options = SimpleNamespace(
            currencies=Currency.objects.all(),
            non_default_plans=self.get_queryset().exclude(is_default=True),
        )

        return Response(AdminPricingPlanCreateOptionsSerializer().to_representation(create_options))
