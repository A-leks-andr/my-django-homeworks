from django.urls import path

from .views import bus_stations, index

urlpatterns = [
    path("", index, name="index"),
    path("bus_stations/", bus_stations, name="bus_stations"),
]
