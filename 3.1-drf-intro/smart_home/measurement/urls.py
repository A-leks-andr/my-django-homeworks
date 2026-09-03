from django.urls import path
from .views import SensorView, SensorDetailView, MeasurementCreateView


urlpatterns = [
    path('sensors/', SensorView.as_view(), name='sensor_list'),
    path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensor-detail'),
    path('measurements/', MeasurementCreateView.as_view(), name='measurement-create'),
]
