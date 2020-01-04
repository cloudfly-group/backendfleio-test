from fleio.celery import app

from django.utils.translation import ugettext_lazy as _
from fleio.reports.location_report import LocationReport
from fleio.core.exceptions import ObjectNotFound
from fleio.reports.models import MonthlyRevenueReport


@app.task(bind=True, max_retries=0, throws=(ObjectNotFound,), name='Generate revenue report',
          resource_type='MonthlyRevenueReport')
def generate_revenue_report(self, monthly_report_id, **kwargs):
    del self, kwargs  # unused
    try:
        monthly_report = MonthlyRevenueReport.objects.get(id=monthly_report_id)
    except MonthlyRevenueReport.DoesNotExist:
        raise ObjectNotFound(_('Could not find monthly revenue report to work with.'))
    location_report = LocationReport(start_date=monthly_report.start_date, end_date=monthly_report.end_date)
    location_report.save_report()
