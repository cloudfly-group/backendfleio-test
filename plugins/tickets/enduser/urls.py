from plugins.tickets.enduser.frontend.views import FrontendView
from plugins.tickets.enduser.tickets.views.tickets import TicketsViewSet, TicketUpdateViewSet
from plugins.tickets.enduser.tickets.views.attachments import TicketAttachmentsViewSet
from plugins.tickets.enduser.tickets.views.departments import DepartmentsViewSet


try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'frontend',
                    FrontendView,
                    basename='frontend',
                    feature_name='plugins.tickets'
                    )

    router.register(r'tickets',
                    TicketsViewSet,
                    basename='tickets',
                    feature_name='plugins.tickets'
                    )
    router.register(r'ticket_updates',
                    TicketUpdateViewSet,
                    basename='ticket_updates',
                    feature_name='plugins.tickets'
                    )
    router.register(r'ticket_attachments',
                    TicketAttachmentsViewSet,
                    basename='ticket_attachments',
                    feature_name='plugins.tickets'
                    )
    router.register(r'departments',
                    DepartmentsViewSet,
                    basename='departments',
                    feature_name='plugins.tickets'
                    )

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
