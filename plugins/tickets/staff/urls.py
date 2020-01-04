from plugins.tickets.staff.frontend.views import FrontendView
from plugins.tickets.staff.tickets.views.tickets import (TicketLinkViewSet, TicketNotesViewSet, TicketsViewSet,
                                                         TicketUpdateViewSet)
from plugins.tickets.staff.tickets.views.attachments import TicketAttachmentsViewSet
from plugins.tickets.staff.tickets.views.departments import DepartmentsViewSet
from plugins.tickets.staff.tickets.views.signatures import StaffSignaturesViewSet


try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
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
    router.register(r'ticket_notes',
                    TicketNotesViewSet,
                    basename='ticket_notes',
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
    router.register(r'ticket_links',
                    TicketLinkViewSet,
                    basename='ticket_links',
                    feature_name='plugins.tickets'
                    )
    router.register(r'staff_signatures',
                    StaffSignaturesViewSet,
                    basename='staff_signatures',
                    feature_name='plugins.tickets'
                    )

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
