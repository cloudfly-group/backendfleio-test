from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.response import Response

from fleio.core.drf import EndUserOnly
from ..summary import get_summary


class SummaryViewSet(viewsets.GenericViewSet):
    permission_classes = (EndUserOnly,)

    def list(self, request):
        return Response(get_summary(request.user))
