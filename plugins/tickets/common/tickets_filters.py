from rest_framework import filters
from plugins.tickets.models.ticket import Ticket


class TicketIdSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search')
        if search and search[0] == '#':
            search = search[1:]
            queryset = Ticket.objects.filter(id__startswith=search)
            return queryset | super().filter_queryset(request=request, queryset=queryset, view=view)
        return super().filter_queryset(request=request, queryset=queryset, view=view)
