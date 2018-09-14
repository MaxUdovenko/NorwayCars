from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.statistics_by_car_maker, name='statistics_by_car_maker'),
]