from django.urls import path
from . import views
from forecast import views

urlpatterns = [
    path('', views.ForecastView.as_view(), name= 'index'),
    path('forecast/', views.ForecastComparisionView.as_view(), name = 'forecast')

]