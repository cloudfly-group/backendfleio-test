from django.conf.urls import include
from django.urls import path

from reseller.openstack.core.views import ResellerOpenstackClientsViewSet
from reseller.openstack.flavors.views.flavor import ResellerFlavorViewSet
from reseller.openstack.images.views.image import ResellerImageViewSet
from reseller.openstack.instances.views.instance import ResellerInstanceViewSet
from reseller.openstack.regions.views.region import ResellerRegionsViewSet
from reseller.openstack.users.views.user import ResellerOpenStackUsersViewSet
from reseller.openstack.ports.views.port import ResellerPortViewSet
from reseller.openstack.volumes.views.volume import ResellerVolumeViewSet
from reseller.osbilling.pricing.views.price_rule import ResellerPriceRuleViewSet
from reseller.osbilling.pricing.views.price_rule_condition import ResellerPriceRuleConditionsViewSet
from reseller.osbilling.pricing.views.price_rule_modifier import ResellerPriceRuleModifiersViewSet
from reseller.osbilling.pricing.views.pricing_plan import ResellerPricingPlanViewSet
from reseller.osbilling.service_dynamic_history.views.service_dynamic_usage import ResellerServiceDynamicUsageViewSet
from reseller.osbilling.service_dynamic_history.views.service_dynamic_usage_history import \
    ResellerServiceDynamicUsageHistoryViewSet

try:
    from fleio.core.loginview import ResellerFeatureRouter

    urlpatterns = list()
    router = ResellerFeatureRouter(trailing_slash=False)

    router.register(
        r'instances',
        ResellerInstanceViewSet,
        basename='instances',
        feature_name='openstack.instances',
    )

    router.register(
        r'ports',
        ResellerPortViewSet,
        basename='ports',
        feature_name='openstack.ports',
    )

    # osbilling routes
    router.register(
        r'billing/usage',
        ResellerServiceDynamicUsageViewSet,
        basename='billing',
        feature_name='billing.history',
    )

    router.register(
        r'billing/usage-history',
        ResellerServiceDynamicUsageHistoryViewSet,
        basename='billing-history',
        feature_name='billing.history',
    )

    router.register(
        r'billing/plan',
        ResellerPricingPlanViewSet,
        basename='billing-plan',
        feature_name='openstack.plans',
    )

    router.register(
        r'billing/pricerule/(?P<pricerule_pk>[^/.]+)/condition',
        ResellerPriceRuleConditionsViewSet,
        basename='billing-pricerulecondition',
        feature_name='openstack.plans',
    )
    router.register(
        r'billing/pricerule/(?P<pricerule_pk>[^/.]+)/modifier',
        ResellerPriceRuleModifiersViewSet,
        basename='billing-pricerulemodifier',
        feature_name='openstack.plans',
    )
    router.register(
        r'billing/pricerule',
        ResellerPriceRuleViewSet,
        basename='billing-pricerule',
        feature_name='openstack.plans',
    )

    # router.register(
    #     r'flavorgroups',
    #     ResellerFlavorGroupViewSet,
    #     basename='flavorgroups',
    #     feature_name='openstack.flavors',
    # )

    router.register(
        r'flavors',
        ResellerFlavorViewSet,
        basename='flavors',
        feature_name='openstack.flavors',
    )

    router.register(
        r'images',
        ResellerImageViewSet,
        basename='images',
        feature_name='openstack.images',
    )

    router.register(
        r'volumes',
        ResellerVolumeViewSet,
        basename='volumes',
        feature_name='openstack.volumes',
    )

    router.register(
        r'clients',
        ResellerOpenstackClientsViewSet,
        basename='clients',
        feature_name='clients&users.clients'
    )

    router.register(
        r'users',
        ResellerOpenStackUsersViewSet,
        basename='users',
        feature_name='openstack.apiusers',
    )

    router.register(
        r'regions',
        ResellerRegionsViewSet,
        basename='regions',
        feature_name='core',
    )

    urlpatterns.extend([
        path('openstack/', include(router.urls)),
    ])

except ImportError:
    urlpatterns = []
