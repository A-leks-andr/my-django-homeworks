from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)

class Sensor(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    description = models.CharField(max_length=150, verbose_name='Описание', blank=True)

    class Meta:
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE,
        related_name='measurements',
        verbose_name="Датчик"
        )
    temperature = models.FloatField(verbose_name="Температура")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время измерения"
        )
    image = models.ImageField(
        upload_to="measurements_images/",
        blank=True, null=True,
        verbose_name="Изображение"
        )

    class Meta:
        verbose_name = "Измерение"
        verbose_name_plural = "Измерения"
        ordering = ['-created_at']

    def __str__(self):
        formatted_date = self.created_at.strftime('%d.%m.%Y %H:%M')
        return f"{self.sensor.name}: {self.temperature}°C ({formatted_date})"