import pytz

from django.conf import settings
from rest_framework import serializers
from .models import ClientRevenueReport
from .models import ClientLocationRevenue
from .models import ServiceRevenueReport
from .models import ServiceEntriesReport
from .models import ServiceUsageDetailsReport
from .models import MonthlyLocationRevenue
from .models import MonthlyRevenueReport


class ServiceUsageDetailsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUsageDetailsReport
        fields = '__all__'


class ServiceEntriesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEntriesReport
        fields = '__all__'


class ServiceRevenueReportSerializer(serializers.ModelSerializer):
    usage_details = ServiceUsageDetailsReportSerializer(required=False, default={})
    entries = ServiceEntriesReportSerializer(many=True)

    class Meta:
        model = ServiceRevenueReport
        fields = '__all__'


class ClientLocationRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLocationRevenue
        fields = '__all__'


class ClientRevenueReportSerializer(serializers.ModelSerializer):
    revenue_per_location = ClientLocationRevenueSerializer(many=True)
    services_report = ServiceRevenueReportSerializer(many=True)

    class Meta:
        model = ClientRevenueReport
        fields = '__all__'


class MonthlyLocationRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyLocationRevenue
        fields = ('name', 'revenue')


class MonthlyRevenueReportSerializer(serializers.ModelSerializer):
    total_revenue_per_location = MonthlyLocationRevenueSerializer(many=True)
    report_month_year = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyRevenueReport
        fields = '__all__'

    @staticmethod
    def get_report_month_year(obj: MonthlyRevenueReport):
        revenue_reporting_timezone = getattr(settings, 'REVENUE_REPORTING_TIMEZONE', None)
        if not revenue_reporting_timezone:
            tz_info = pytz.timezone(getattr(settings, 'TIME_ZONE'))
        else:
            tz_info = pytz.timezone(revenue_reporting_timezone)
        return obj.start_date.astimezone(tz_info).strftime("%B %Y")


class MonthlyRevenueReportDetailsSerializer(serializers.ModelSerializer):
    total_revenue_per_location = MonthlyLocationRevenueSerializer(many=True)
    revenue_report = ClientRevenueReportSerializer(many=True, read_only=True)
    report_month_year = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyRevenueReport
        fields = '__all__'

    @staticmethod
    def get_report_month_year(obj: MonthlyRevenueReport):
        revenue_reporting_timezone = getattr(settings, 'REVENUE_REPORTING_TIMEZONE', None)
        if not revenue_reporting_timezone:
            tz_info = pytz.timezone(getattr(settings, 'TIME_ZONE'))
        else:
            tz_info = pytz.timezone(revenue_reporting_timezone)
        return obj.start_date.astimezone(tz_info).strftime("%B %Y")
