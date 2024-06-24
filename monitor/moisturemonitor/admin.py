from django.contrib import admin
from moisturemonitor.models import MoistureMonitor

class MoistureMonitorAdmin(admin.ModelAdmin):
    search_fields = ('parcel', 'name', 'date')
    date_hierarchy = 'date'
    list_display = ('pk', 'parcel', 'name', 'date', 'image', 'nubesImage', 'trueColorImage')
    list_display_links = ('pk', 'parcel', 'name', 'date', 'image', 'nubesImage', 'trueColorImage')
admin.site.register(MoistureMonitor, MoistureMonitorAdmin)