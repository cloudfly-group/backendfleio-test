from plugins.domains.enduser.frontend.components.views import FrontendView
from plugins.domains.enduser.views.contacts import ContactsViewSet
from plugins.domains.enduser.views.domains import DomainsViewSet
from plugins.domains.enduser.views.order_domain import OrderDomainViewSet

try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'frontend', FrontendView, basename='frontend', feature_name='plugins.domains')

    router.register(r'contacts', ContactsViewSet, basename='contacts', feature_name='plugins.domains')
    router.register(r'domains', DomainsViewSet, basename='domains', feature_name='plugins.domains')
    router.register(r'order-domain', OrderDomainViewSet, basename='order-domain', feature_name='plugins.domains')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
