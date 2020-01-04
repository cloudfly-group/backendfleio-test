from rest_framework import viewsets
from rest_framework.response import Response

from fleio.core.drf import StaffOnly


class CPanelLicenseViews(viewsets.ViewSet):
    permission_classes = (StaffOnly,)

    def list(self, request):
        return Response(['List cPanel licenses'])
