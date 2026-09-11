from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement, Favorite
from .permissions import IsOwnerOrReadOnly
from .serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    def get_queryset(self):
        self.queryset = Advertisement.objects.all()
        user = self.request.user

        if user.is_authenticated and user.is_staff:
            return self.queryset

        if user.is_authenticated:
            return self.queryset.filter(
                Q(status__in=["OPEN", "CLOSED"]) | Q(creator=user)
            )

        return self.queryset.filter(status__in=["OPEN", "CLOSED"])


class FavoriteViewSet(ModelViewSet):
    """Управление избранными объявлениями."""

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
