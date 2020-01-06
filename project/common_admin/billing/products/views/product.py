from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import ProtectedError
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.billing.models import ConfigurableOption
from fleio.billing.models import Product
from fleio.billing.models import ProductConfigurableOption
from fleio.billing.models import ProductGroup
from fleio.billing.models import ProductModule
from fleio.billing.settings import PricingModel
from fleio.billing.settings import ProductAutoSetup
from fleio.billing.settings import ProductType
from fleio.billing.settings import PublicStatuses
from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import APIConflict
from fleio.core.exceptions import ObjectNotFound
from fleio.core.features import staff_active_features
from fleio.core.plugins.plugin_utils import PluginUtils
from fleiostaff.billing.products.serializers import ProductUpgradesSerializer
from fleiostaff.billing.products.serializers import StaffAssociateConfigurableOption
from fleiostaff.billing.products.serializers import StaffProductConfigurableOptionSerializer
from fleiostaff.billing.products.serializers import StaffProductCreateSerializer
from fleiostaff.billing.products.serializers import StaffProductDetailSerializer
from fleiostaff.billing.products.serializers import StaffProductSerializer
from fleiostaff.billing.products.serializers import StaffProductUpdateSerializer


class AdminProductViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = StaffProductSerializer
    serializer_map = {'create': StaffProductCreateSerializer,
                      'update': StaffProductUpdateSerializer,
                      'retrieve': StaffProductDetailSerializer}
    model = Product
    queryset = StaffProductSerializer.Meta.model.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('name', 'description', 'code', 'status', 'price_model')
    ordering_fields = ('name', 'description', 'code', 'status', 'price_model')
    search_fields = ('name', 'description', 'code', 'status', 'price_model')
    ordering = ['name']

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(group__visible=True).all()

        return self.queryset

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=False, methods=['GET'])
    def create_options(self, request):
        del request  # unused
        options = dict()
        options['groups'] = [{'id': group.id, 'name': group.name, 'description': group.description} for group in
                             ProductGroup.objects.filter(visible=True).all()]
        if not options['groups']:
            raise ObjectNotFound('No product groups exist')
        modules_queryset = ProductModule.objects.filter(
            plugin__enabled=True
        ).exclude(plugin__staff_feature_name__in=staff_active_features.get_disabled_features())
        options['modules'] = {
            module.id:
            {
                'id': module.id,
                'name': module.name,
                'plugin': module.plugin_label if module.plugin_label and PluginUtils.has_staff_component(
                    plugin_label=module.plugin_label,
                    component_name='ProductSettings'
                ) else None,
                'description': module.description
            }
            for module in modules_queryset
        }
        if not options['modules']:
            raise ObjectNotFound('No product modules exist')

        options['product_types'] = ProductType.choices
        options['statuses'] = PublicStatuses.choices
        options['price_models'] = PricingModel.choices
        options['auto_setups'] = ProductAutoSetup.choices

        return Response(options)

    def perform_destroy(self, instance):
        with transaction.atomic():
            if instance.services.count() > 0:
                raise APIConflict(_("Can't delete product in use by services"))
            try:
                instance.cycles.all().delete()
            except ProtectedError:
                # TODO: maybe return the objects which reference the cycles (exception.protected_objects)
                raise APIConflict(_("Can't delete product in use by services"))
            instance.delete()

    @action(methods=['GET'], detail=True)
    def configurable_options(self, request, pk):
        del request, pk  # unused
        product = self.get_object()
        ser = StaffProductConfigurableOptionSerializer(many=True, context={'product': product})
        available_options = ConfigurableOption.objects.exclude(products__id=product.id).exclude(visible=False)
        return Response({'configurable_options': ser.to_representation(product.configurable_options.all()),
                         'available_options': ser.to_representation(available_options.all())})

    @action(methods=['POST'], detail=True)
    def associate_configurable_option(self, request, pk):
        self.get_object()  # NOTE(tomo): leave this for permission checks
        association = {'product': pk, 'configurable_option': request.data.get('configurable_option')}
        ser = StaffAssociateConfigurableOption(data=association)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'detail': _('Option associated')})

    @action(methods=['POST'], detail=True)
    def dissociate_configurable_option(self, request, pk):
        del pk  # unused
        product = self.get_object()
        option_id = request.data.get('option', None)
        if option_id is None:
            raise APIBadRequest(_('No option provided'))
        try:
            option_id = int(option_id)
        except ValueError:
            raise APIBadRequest(_('Option does not exist'))
        if product.configurable_options.filter(id=option_id).exists() == 0:
            raise APIConflict(_('Option not associated with product'))
        ProductConfigurableOption.objects.filter(product=product, configurable_option__id=option_id).delete()
        return Response({'detail': _('Option dissociated')})

    @action(methods=['GET', 'POST'], detail=True)
    def upgrade_options(self, request, pk):
        del pk  # unused
        product = self.get_object()  # Type: Product
        empty_response = {'available_products': [],
                          'selected_products': []}
        if request.method == 'GET':
            if product.module:
                try:
                    upgrade_list = Product.objects.exclude(pk=product.pk).filter(module=product.module)
                    selected_products = product.upgrades.values('id', 'name')
                except ObjectDoesNotExist:
                    return Response(empty_response)
                else:
                    return Response({'available_products': upgrade_list.values('id', 'name'),
                                     'selected_products': selected_products})
            else:
                return Response(empty_response)
        else:
            ser = ProductUpgradesSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            upgrade_list = ser.validated_data.get('upgrades', [])
            if upgrade_list:
                product.upgrades.set(upgrade_list)
            else:
                product.upgrades.clear()
            return Response({'detail': 'Ok'})
