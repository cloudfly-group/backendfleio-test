from django.urls import path

from fleio.billing.taxrules.views import get_applicable_tax_rules
from fleio.core.features import active_features
from fleio.billing.products.view import ProductViewset
from fleio.billing.views import billing_summary_view
from fleio.billing.cart.views import cartview
from fleio.billing.cart.views import create_order
from fleio.billing.cart.views import CartItemViewSet
from fleio.billing.invoicing.views import InvoiceViewSet
from fleio.billing.gateways.views import GatewaysViewset
from fleio.billing.gateways.views import callback
from fleio.billing.gateways.views import action
from fleio.billing.services.views import ServicesViewset

try:
    from fleio.core.loginview import FeatureRouter

    router = FeatureRouter(trailing_slash=False)
    router.register(r'billing/products', ProductViewset, basename='products', feature_name='billing.order')
    router.register(r'billing/cart/items', CartItemViewSet, basename='cartitems', feature_name='billing.order')
    router.register(r'billing/invoices', InvoiceViewSet, basename='invoices', feature_name='billing.invoices')
    router.register(r'billing/gateways', GatewaysViewset, basename='gateways', feature_name='core')
    router.register(r'billing/services', ServicesViewset, basename='services', feature_name='billing.services')
    urlpatterns = router.urls

    if active_features.is_enabled('billing.order'):
        urlpatterns.append(path('billing/cart/order', create_order, name='cartorder'))
        urlpatterns.append(path('billing/cart', cartview, name='cartview'))

    urlpatterns.append(path('billing/taxrules', get_applicable_tax_rules, name='taxrules'))

    # NOTE(tomo): summary as a simple view
    urlpatterns.append(path('billing/summary', billing_summary_view, name='billing-summary'))
    # NOTE(tomo): gateways generic urls
    urlpatterns.append(path('billing/gateway/<slug:gateway>/callback', callback, name='gateway-callback'))
    urlpatterns.append(path('billing/gateway/<slug:gateway>/<slug:action_name>', action, name='gateway-action'))

except ImportError as e:
    urlpatterns = []
