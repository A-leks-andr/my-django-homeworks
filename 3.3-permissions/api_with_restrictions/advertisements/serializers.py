from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
        )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        status = data.get("status", self.instance.status if self.instance else "OPEN")
        if status == "OPEN":
            user = self.context["request"].user
            open_adv_count = Advertisement.objects.filter(
                creator=user, status="OPEN"
            ).count()

            if self.instance and self.instance.status == "OPEN":
                open_adv_count -= 1

            if open_adv_count >= 10:
                raise ValidationError(
                    {
                        "status": "У вас не может быть более "
                        "10 открытых объявлений одновременно"
                    }
                )

        return data


class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ["id", "advertisement"]

    def validate(self, data):
        user = self.context["request"].user
        advertisement = data["advertisement"]

        if advertisement.creator == user:
            raise ValidationError(
                "Вы не можете добавить собственное объявление в избранное."
            )

        if Favorite.objects.filter(user=user, advertisement=advertisement).exists():
            raise ValidationError(
                "Это объявление уже находится в вашем списке избранного."
            )
        return data
