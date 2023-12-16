from django.contrib import admin

# Register your models here.
from vendor.models import Vendor, HistoricalPerformance

admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)