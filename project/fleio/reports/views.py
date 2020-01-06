from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIBadRequest, APIConflict, ConfigurationError
from fleio.core.filters import CustomFilter
from fleio.reports.models import MonthlyRevenueReport
from fleio.reports.serializers import MonthlyRevenueReportDetailsSerializer
from .serializers import MonthlyRevenueReportSerializer

from fleio.reports.revenue_report_generation import generate_revenue_report
from fleio.reports.exceptions import InvalidArgument, ReportIsAlreadyGenerating, RevenueReportTimezoneError


# TODO: move this to staff
@log_staff_activity(category_name='reports', object_name='report')
class RevenueReportsViewset(viewsets.ModelViewSet):
    serializer_class = MonthlyRevenueReportSerializer
    queryset = MonthlyRevenueReport.objects.all()
    permission_classes = (CustomPermissions, StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('revenue_report__client__first_name', 'revenue_report__client__last_name')
    ordering_fields = ('start_date', 'end_date')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MonthlyRevenueReportDetailsSerializer
        else:
            return self.serializer_class

    @action(methods=['POST'], detail=False)
    def trigger_revenue_report_generation(self, request):
        month = request.data.get('month', None)
        year = request.data.get('year', None)
        if month is None or year is None:
            raise APIBadRequest(_('Missing year or month.'))
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            raise APIBadRequest(_('Year and month should be integer values'))

        month_and_year = '{}/{}'.format(month, year)
        try:
            generate_revenue_report(month_and_year=month_and_year)
        except InvalidArgument as e:
            raise APIBadRequest(str(e))
        except ReportIsAlreadyGenerating as e:
            raise APIConflict(str(e))
        except RevenueReportTimezoneError as e:
            raise ConfigurationError(str(e))
        else:
            reports_under_generation = MonthlyRevenueReport.objects.filter(generating=True)
            if reports_under_generation:
                reports_under_generation_representation = MonthlyRevenueReportSerializer(
                    instance=reports_under_generation,
                    many=True,
                    read_only=True
                ).data
            else:
                reports_under_generation_representation = []

        return Response({
            'detail': 'OK',
            'reports_under_generation': reports_under_generation_representation
        })
