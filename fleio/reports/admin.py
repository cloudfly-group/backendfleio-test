from django.contrib import admin

from .models import MonthlyLocationRevenue
from .models import MonthlyRevenueReport
from .models import ClientRevenueReport
from .models import ClientLocationRevenue
from .models import ServiceRevenueReport
from .models import ServiceUsageDetailsReport
from .models import ServiceEntriesReport


admin.site.register(MonthlyLocationRevenue)
admin.site.register(MonthlyRevenueReport)
admin.site.register(ClientRevenueReport)
admin.site.register(ClientLocationRevenue)
admin.site.register(ServiceRevenueReport)
admin.site.register(ServiceUsageDetailsReport)
admin.site.register(ServiceEntriesReport)
