from celery import shared_task
from forecast.services import ForecastService

@shared_task

def update_data_periodically():
    ForecastService.fetch_and_update_data()