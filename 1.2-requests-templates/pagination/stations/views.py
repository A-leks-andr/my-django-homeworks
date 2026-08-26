from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv

BUS_STATIONS = []
with open(settings.BUS_STATION_CSV, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        BUS_STATIONS.append(row)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(BUS_STATIONS, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
