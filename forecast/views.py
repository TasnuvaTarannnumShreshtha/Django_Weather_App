from django.shortcuts import render
import json
import requests
from .raw_districts_data import data_of_districts
from datetime import date

# Create your views here.

def index(request):
    data_of_all_districts = data_of_districts['districts'] 
    temperature_of_all_districts = {}   

    for district in data_of_all_districts:
        lat = district['lat']
        long = district['long']
        district_name = district['name']
        
        api_url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat +'&longitude='+ long +'&hourly=temperature_2m&' 
        reponse = requests.get(api_url)
        json_data = reponse.json()
        hourly_temperature_data = json_data['hourly']['temperature_2m']
        length_of_hourly_temperature_data = len(hourly_temperature_data)

        temperatures_at_2PM = []

        for i in range(13, length_of_hourly_temperature_data, 24):
            input_number = round(hourly_temperature_data[i], 2)
            temperatures_at_2PM.append(input_number)

        sum_of_temperatures = sum(temperatures_at_2PM)
        average_temperature = sum_of_temperatures / 7
        temperature_of_all_districts[district_name] = round(average_temperature, 2)


    sorted_temperature_of_all_districts = sorted(temperature_of_all_districts.items(), key = lambda x:x[1])
    top_10_coolest_districts = sorted_temperature_of_all_districts[:10]
    name_of_coolest_disticts = []


    for district in top_10_coolest_districts:
        name_of_coolest_disticts.append(district[0])
        
    
    coolest_district = name_of_coolest_disticts[0]


    return render(request, 'forecast/index.html', {'lat':lat, 'long':long,
                                         'hourly_temperatures':hourly_temperature_data,
                                         'length_of_all_data':length_of_hourly_temperature_data,
                                         'temperatures_at_2PM': temperatures_at_2PM,
                                         'average_temperature':average_temperature,
                                         'temperature_of_all_districts': sorted_temperature_of_all_districts,
                                         'top_10_coolest_districts': top_10_coolest_districts,
                                         'name_of_coolest_districts': name_of_coolest_disticts,
                                         'coolest_district': coolest_district
                                         })


def forecast(request):

    if request.method == "GET":
        location = request.GET.get('location')
        destination = request.GET.get('destination')
        date_of_travel = request.GET.get('date_of_travel')
        long_of_location = 0
        lat_of_location = 0
        long_of_dest = 0
        lat_of_dest = 0
        for district in data_of_districts['districts']:
            if(district['name'] == location):
                long_of_location = district['long']
                lat_of_location = district['lat']
            if(district['name'] == destination):
                long_of_dest = district['long']
                lat_of_dest = district['lat']

        
        today = date.today()
        start_hour_today = str(today) + "T14:00"
        start_hour_travel_day = str(date_of_travel) + "T14:00"
        
        api_url = "https://api.open-meteo.com/v1/forecast?latitude="+ str(lat_of_location) + "&longitude="+ str(long_of_location) +"&hourly=temperature_2m&start_hour=" + start_hour_today +"&end_hour=" + start_hour_today
        response = requests.get(api_url)
        json_data = response.json()
        location_temperature_at_2PM = json_data['hourly']['temperature_2m']

        api_url = "https://api.open-meteo.com/v1/forecast?latitude="+ str(lat_of_dest) +"&longitude="+ str(long_of_dest) +"&hourly=temperature_2m&start_hour=" + start_hour_travel_day + "&end_hour=" + start_hour_travel_day
        response = requests.get(api_url)
        json_data = response.json()
        destination_temperature_at_2PM = json_data['hourly']['temperature_2m']

        return render(request, 'forecast/forecast.html', {'location_temperature_at_2PM': location_temperature_at_2PM, 'destination_temperature_at_2PM': destination_temperature_at_2PM})
    
    return render(request, 'forecast/forecast.html')
    