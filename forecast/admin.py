from django.contrib import admin
from forecast.models import TemperatureData

class TemperatureDataAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'longitude', 'latitude', 'date_created', 'average_temperature')
    readonly_fields = ('date_created',)

admin.site.register(TemperatureData, TemperatureDataAdmin)
