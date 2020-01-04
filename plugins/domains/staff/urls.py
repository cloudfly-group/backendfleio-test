from plugins.domains.staff.frontend.views import FrontendView
from plugins.domains.staff.views.contacts import ContactsViewSet
from plugins.domains.staff.views.domains import DomainsViewSet
from plugins.domains.staff.views.order_domain import OrderDomainViewSet
from plugins.domains.staff.views.registrar_connectors import RegistrarConnectorsViewSet
from plugins.domains.staff.views.registrar_prices import RegistrarPricesViewset
from plugins.domains.staff.views.registrars import RegistrarsViewSet
from plugins.domains.staff.views.tlds import TLDsViewSet

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'frontend', FrontendView, basename='frontend', feature_name='plugins.domains')

    router.register(r'contacts', ContactsViewSet, basename='contacts', feature_name='plugins.domains')
    router.register(r'domains', DomainsViewSet, basename='domains', feature_name='plugins.domains')
    router.register(r'registrars', RegistrarsViewSet, basename='registrars', feature_name='plugins.domains')
    router.register(r'registrar_prices', RegistrarPricesViewset, basename='registrar_prices',
                    feature_name='plugins.domains')
    router.register(
        r'registrar_connectors',
        RegistrarConnectorsViewSet,
        basename='registrar_connectors',
        feature_name='plugins.domains',
    )
    router.register(r'tlds', TLDsViewSet, basename='tlds', feature_name='plugins.domains')
    router.register(r'order-domain', OrderDomainViewSet, basename='order-domain', feature_name='plugins.domains')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
