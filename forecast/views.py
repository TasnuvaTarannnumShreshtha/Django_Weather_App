import logging
from django.views import View
from django.shortcuts import render
import json
import requests
from forecast.raw_districts_data import data_of_districts
from datetime import date
from django.conf import settings
from forecast.services import ForecastService
from forecast.models import TemperatureData

logger = logging.getLogger('views')

class ForecastView(View):
    def get(self, request):
        district_instances = TemperatureData.objects.filter(district_name = 'Dhaka', date_created__date = date.today())
        
        # if data exists in database just call them from Forecast service
        if district_instances.exists():
            top_10_coolest_districts = ForecastService.fetch_sorted_instances()
        # if database is empty fetch it from the api using Forecast service
        else:
            top_10_coolest_districts = ForecastService.fetch_coolest_temperatures()

        ten_coolest_districts = {}

        for each_district in top_10_coolest_districts[:10]:
            ten_coolest_districts[each_district['district_name']] = each_district['average_temperature']
        
        coolest_district = list(ten_coolest_districts.items())[0]
        return render(request, 'forecast/index.html', {
                                            'top_10_coolest_districts': ten_coolest_districts,
                                            'coolest_district': coolest_district
                                            })

class ForecastComparisionView(View):
    def get(self, request):
        if not request.GET.get('date_of_travel'):
            logger.warning("No date of travel provided")
            error_message = "Please enter a date of travel"
            return render(request, 'forecast/forecast.html', {'error_message':error_message})
        
        location = request.GET.get('location')
        destination = request.GET.get('destination')
        date_of_travel = request.GET.get('date_of_travel')
        location_temperature_at_2PM = ForecastService.forecast_location_weather(location, date_of_travel)
        destination_temperature_at_2PM = ForecastService.forecast_location_weather(destination, date_of_travel)
        return render(request, 'forecast/forecast.html', {
                                                        'location_temperature_at_2PM': location_temperature_at_2PM, 
                                                        'location_name': location, 'destination_name': destination,
                                                        'destination_temperature_at_2PM': destination_temperature_at_2PM,
                                                        'date_of_travel': date_of_travel
                                                        })
        
        
        