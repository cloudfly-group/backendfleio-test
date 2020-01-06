from django.conf.urls import include, url

from fleio.core.features import active_features

from fleio.openstack.dns.views import DnsViewSet
from fleio.openstack.images.views import ImageViewSet
from fleio.openstack.instances.views import InstanceViewSet
from fleio.openstack.networking.views import FloatingIpViewSet
from fleio.openstack.networking.views import NetworkViewSet
from fleio.openstack.networking.views import RouterViewSet
from fleio.openstack.networking.views import SecurityGroupViewSet
from fleio.openstack.networking.views import SubnetViewSet
from fleio.openstack.ports.views import PortViewSet
from fleio.openstack.volume_snapshots.views import VolumeSnapshotViewSet
from fleio.openstack.volumes.views import VolumesViewSet
from fleio.openstack.volume_backups.views import VolumeBackupViewSet
from fleio.openstack.views import regions, summary
from fleio.openstack.users.views import OpenStackUsersViewSet
from fleio.openstack.container_infra.cluster_templates.views import EndUserClusterTemplateViewSet
from fleio.openstack.container_infra.clusters.views import EndUserClusterViewSet

try:
    from ..core.loginview import OpenstackRouter
    router = OpenstackRouter(trailing_slash=False)
    router.register(r'floatingips', FloatingIpViewSet, basename='floatingips', feature_name='openstack.floatingips')
    router.register(r'networks', NetworkViewSet, basename='networks', feature_name='openstack.networks')
    router.register(r'routers', RouterViewSet, basename='routers', feature_name='openstack.routers')
    router.register(r'securitygroups', SecurityGroupViewSet, basename='securitygroups',
                    feature_name='openstack.securitygroups')
    router.register(r'subnets', SubnetViewSet, basename='subnets', feature_name='core')
    router.register(r'ports', PortViewSet, basename='ports', feature_name='openstack.ports')
    router.register(r'instances', InstanceViewSet, basename='instances', feature_name='openstack.instances')
    router.register(r'images', ImageViewSet, basename='images', feature_name='openstack.images')
    router.register(r'volumes', VolumesViewSet, basename='volumes', feature_name='openstack.volumes')
    router.register(r'volumebackups', VolumeBackupViewSet, basename='volumebackups',
                    feature_name='openstack.volumes.backups')
    router.register(r'volumesnapshots', VolumeSnapshotViewSet, basename='volumesnapshots',
                    feature_name='openstack.volumes.snapshots')
    router.register(r'summary', summary.SummaryViewSet, basename='summary', feature_name='core')
    router.register(r'regions', regions.RegionsViewSet, basename='regions', feature_name='core')
    router.register(r'users', OpenStackUsersViewSet, basename='apiusers', feature_name='openstack.apiusers')
    router.register(r'dns', DnsViewSet, basename='dns', feature_name='openstack.dns.zones')
    router.register(r'cluster-templates', EndUserClusterTemplateViewSet, basename='clustertemplates',
                    feature_name='openstack.coe.cluster_templates')
    router.register(r'clusters', EndUserClusterViewSet, basename='clusters', feature_name='openstack.coe.clusters')

    try:
        from fleio.osbilling.views import ServiceDynamicUsageViewset, ServiceDynamicUsageHistoryViewset
        router.register(r'billing/history', ServiceDynamicUsageHistoryViewset,
                        basename='billing-history', feature_name='billing.history')
        router.register(r'billing', ServiceDynamicUsageViewset, basename='billing', feature_name='billing.history')
    except ImportError as e:
        pass

    if not active_features.is_enabled('openstack.instances.snapshots'):
        # TODO(tomo): Fix this handling of snapshots as a feature
        snapshot_url_list = list(filter(lambda link: link.name == u'instances-create-snapshot', router.urls))
        if snapshot_url_list:
            del router.urls[router.urls.index(snapshot_url_list[0])]

    urlpatterns = [
        url(r'^openstack/', include(router.urls)),
    ]
except ImportError:
    urlpatterns = []
