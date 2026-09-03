from rest_framework import serializers
from .models import Sensor, Measurement

# TODO: опишите необходимые сериализаторы

class MeasurementSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", read_only=True) # type: ignore
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at', 'image']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']