from django.db import models
import json
from django.utils import timezone

class TemperatureData(models.Model):
    district_name = models.CharField(max_length=100, primary_key = True, unique=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    date_created = models.DateTimeField(auto_now = True)
    temperature = models.JSONField(default=list)
    average_temperature = models.IntegerField(null=True)