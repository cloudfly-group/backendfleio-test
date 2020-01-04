from django.conf.urls import include
from django.urls import path

from fleio.core.features import staff_active_features

from fleiostaff.openstack.conf.views import OpenstackConfigurationsViewSet
from fleiostaff.openstack.container_infra.cluster_templates.views import StaffClusterTemplateViewSet
from fleiostaff.openstack.container_infra.clusters.views import StaffClusterViewSet
from fleiostaff.openstack.core.views import OpenstackClientsViewSet
from fleiostaff.openstack.dns.views import DnsViewSet
from fleiostaff.openstack.flavorgroups.views import FlavorGroupViewSet
from fleiostaff.openstack.flavors.views import FlavorViewSet
from fleiostaff.openstack.floatingips.views import StaffFloatingIpViewSet
from fleiostaff.openstack.images.views import StaffImageViewSet
from fleiostaff.openstack.instances.views import StaffInstanceViewSet
from fleiostaff.openstack.networks.views import StaffNetworkViewSet
from fleiostaff.openstack.ports.views import StaffPortViewSet
from fleiostaff.openstack.projects.views import StaffProjectViewSet
from fleiostaff.openstack.regions.views import StaffRegionsViewSet
from fleiostaff.openstack.routers.views import StaffRouterViewSet
from fleiostaff.openstack.securitygroups.views import StaffSecurityGroupViewSet
from fleiostaff.openstack.settings.views import credentials_view
from fleiostaff.openstack.settings.views import defaults_view
from fleiostaff.openstack.settings.views import notifications_view
from fleiostaff.openstack.settings.views import services
from fleiostaff.openstack.settings.views import test_notifications_connections
from fleiostaff.openstack.settings.views import test_connection
from fleiostaff.openstack.settings.views import volume_size_increments
from fleiostaff.openstack.subnetpools.views import StaffSubnetPoolViewSet
from fleiostaff.openstack.subnets.views import StaffSubnetViewSet
from fleiostaff.openstack.users.views import StaffOpenStackUsersViewSet
from fleiostaff.openstack.volume_snapshots.views import StaffVolumeSnapshotViewSet
from fleiostaff.openstack.volumes.views import StaffVolumeViewSet
from fleiostaff.openstack.volume_backups.views import VolumeBackupViewSet
from fleiostaff.osbilling.views import PriceRuleConditionsViewset
from fleiostaff.osbilling.views import PriceRuleModifiersViewset
from fleiostaff.osbilling.views import PriceRuleViewset
from fleiostaff.osbilling.views import PricingPlanViewset
from fleiostaff.osbilling.views import StaffClientBillingHistoryViewset
from fleiostaff.osbilling.views import StaffClientBillingViewset
from fleiostaff.openstack.summary_views import operating_systems_summary_view
from fleiostaff.openstack.summary_views import hypervisors_summary_view
from fleiostaff.openstack.hypervisors.views import HypervisorsListRetrieveViewSet

try:
    from fleio.core.loginview import StaffFeatureRouter

    urlpatterns = list()
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'clients', OpenstackClientsViewSet, basename='clients', feature_name='clients&users.clients')
    router.register(r'configurations', OpenstackConfigurationsViewSet,
                    basename='configurations', feature_name='settings.configurations')
    router.register(r'instances', StaffInstanceViewSet, basename='instances', feature_name='openstack.instances')
    router.register(r'ports', StaffPortViewSet, basename='ports', feature_name='openstack.ports')
    router.register(r'projects', StaffProjectViewSet, basename='projects', feature_name='openstack.projects')
    router.register(r'routers', StaffRouterViewSet, basename='routers', feature_name='openstack.routers')
    router.register(r'flavorgroups', FlavorGroupViewSet, basename='flavorgroups', feature_name='openstack.flavors')
    router.register(r'flavors', FlavorViewSet, basename='flavors', feature_name='openstack.flavors')
    router.register(r'floatingips', StaffFloatingIpViewSet, basename='floatingips',
                    feature_name='openstack.floatingips')
    router.register(r'images', StaffImageViewSet, basename='images', feature_name='openstack.images')
    router.register(r'volumes', StaffVolumeViewSet, basename='volumes', feature_name='openstack.volumes')
    router.register(r'volumebackups', VolumeBackupViewSet, basename='volumebackups',
                    feature_name='openstack.volumes.backups')
    router.register(r'volumesnapshots', StaffVolumeSnapshotViewSet, basename='volumesnapshots',
                    feature_name='openstack.volumes.snapshots')
    router.register(r'regions', StaffRegionsViewSet, basename='regions', feature_name='core')
    router.register(r'networks', StaffNetworkViewSet, basename='networks', feature_name='openstack.networks')
    router.register(r'securitygroups', StaffSecurityGroupViewSet, basename='securitygroups',
                    feature_name='openstack.securitygroups')
    router.register(r'subnets', StaffSubnetViewSet, basename='subnets', feature_name='openstack.subnets')
    router.register(r'dns', DnsViewSet, basename='dns', feature_name='openstack.dns.zones')
    router.register(r'subnetpools', StaffSubnetPoolViewSet, basename='subnetpools',
                    feature_name='openstack.subnetpools')
    router.register(r'users', StaffOpenStackUsersViewSet, basename='apiusers', feature_name='openstack.apiusers')
    router.register(r'hypervisors', HypervisorsListRetrieveViewSet, basename='hypervisors', feature_name='openstack')
    router.register(r'cluster-templates', StaffClusterTemplateViewSet, basename='clustertemplates',
                    feature_name='openstack.coe.cluster_templates')
    router.register(r'clusters', StaffClusterViewSet, basename='clusters', feature_name='openstack.coe.clusters')

    # TODO: see if commented out views are used anymore and if not delete them
    # router.register(r'billing/resource', ResourceViewset, basename='billing-resource', feature_name='billing')
    router.register(
        r'billing/plan', PricingPlanViewset, basename='billing-plan', feature_name='openstack.plans'
    )
    router.register(r'billing/pricerule/(?P<pricerule_pk>[^/.]+)/condition', PriceRuleConditionsViewset,
                    basename='billing-pricerulecondition', feature_name='openstack.plans')
    router.register(r'billing/pricerule/(?P<pricerule_pk>[^/.]+)/modifier', PriceRuleModifiersViewset,
                    basename='billing-pricerulemodifier', feature_name='openstack.plans')
    router.register(
        r'billing/pricerule', PriceRuleViewset, basename='billing-pricerule', feature_name='openstack.plans'
    )
    router.register(r'billing/history', StaffClientBillingHistoryViewset,
                    basename='billing-history', feature_name='core')
    router.register(r'billing/(?P<billing_id>[^/.]+)/history', StaffClientBillingHistoryViewset,
                    basename='billing-history', feature_name='core')
    router.register(r'billing', StaffClientBillingViewset, basename='billing', feature_name='core')

    if staff_active_features.is_enabled('openstack.settings'):
        urlpatterns.extend([
            path('settings/openstack/test_connection', test_connection, name='test_openstack_connection'),
            path('settings/openstack/notifications', notifications_view, name='openstack_notifications'),
            path('settings/openstack/test-notifications-connections', test_notifications_connections,
                 name='test-notifications-connections'),
            path('settings/openstack/defaults', defaults_view, name='openstack_defaults'),
            path('settings/openstack/services', services, name='openstack_services'),
            path('settings/openstack/volume_size_increments', volume_size_increments, name='volume_size_increments'),
            path('settings/openstack', credentials_view, name='openstack_settings'),
        ])

    urlpatterns.extend([
        path('openstack/', include(router.urls)),
        path('openstack/summary/operating_systems', operating_systems_summary_view, name='os-summary'),
        path('openstack/summary/hypervisors', hypervisors_summary_view, name='hypervisors-summary'),
    ])

except ImportError:
    urlpatterns = []
