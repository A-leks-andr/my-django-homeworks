from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.DRAFT,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Объявление {self.pk}: {self.title}"


class Favorite(models.Model):
    """Модель для избранных объявлений."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        unique_together = ("user", "advertisement")

    def __str__(self):
        return f"""Пользователь {self.user.username} 
                добавил в избранное {self.advertisement.title}"""
