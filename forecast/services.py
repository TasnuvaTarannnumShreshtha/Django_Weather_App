import logging
from forecast.raw_districts_data import data_of_districts
from django.conf import settings
import requests
import json
from forecast.models import TemperatureData
from datetime import date, datetime

logger = logging.getLogger('services')

class ForecastService:
    def build_api_route(lat, long, district_name):
        api_url = f"{settings.API_URL}latitude={lat}&longitude={long}&hourly=temperature_2m&forecast_days=16" 
        return api_url
    
    def fetch_sorted_instances():
        sorted_instances = TemperatureData.objects.all().order_by('average_temperature').values()
        return sorted_instances

    def fetch_and_update_data():
        logger.info("Successfully updating data in models")
        data_of_all_districts = data_of_districts['districts'] 

        for district in data_of_all_districts:
            district_name = district['name']
            lat = district['lat']
            long = district['long']

            api_url = ForecastService.build_api_route(lat, long, district_name)
            reponse = requests.get(api_url)
            json_data = reponse.json()
            hourly_temperature_data = json_data['hourly']['temperature_2m']
            serialized_temperature = json.dumps(hourly_temperature_data) # json format now
            
            temperature_instance = TemperatureData()
            temperature_instance.district_name = district_name
            temperature_instance.longitude = long
            temperature_instance.latitude = lat
            temperature_instance.temperature = serialized_temperature
            temperature_instance.save() 

            temp_instance = TemperatureData.objects.get(pk=district_name)
            deserialized_list_of_temperatures = json.loads(temp_instance.temperature)
            hours_in_7_days = 7 * 24
            temp_at_2PM = []

            # getting temperature values only at 2 PM
            for i in range(13, hours_in_7_days, 24):
                temp_at_2PM.append(deserialized_list_of_temperatures[i])
            
            sum_of_temperatures = sum(temp_at_2PM)
            average_temperature = sum_of_temperatures / 7
            temp_instance.average_temperature = average_temperature
            temp_instance.save()
    
    def fetch_coolest_temperatures():
        ForecastService.fetch_and_update_data()
        sorted_instances = ForecastService.fetch_sorted_instances()
        return sorted_instances

    def forecast_location_weather(location, date_of_travel):
        date_today = date.today()
        date_format = "%Y-%m-%d"
        date_of_travel = datetime.strptime(date_of_travel, date_format)
        date_of_travel = date_of_travel.date()
        time_delta_object = date_of_travel - date_today
        
        difference_of_hours_between_two_days = time_delta_object.days
        hours_elapsed = difference_of_hours_between_two_days * 24
        two_pm = 13

        district_instance = TemperatureData.objects.get(pk = location)
        deserialized_list_of_temperatures = json.loads(district_instance.temperature)
        temperature_at_2PM = deserialized_list_of_temperatures[hours_elapsed + two_pm]

        return temperature_at_2PM


     