from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingPostSerializer

#
# class CreateDestroyAPIView(DestroyAPIView, CreateModelMixin):
#     pass


class BookingViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin,
                     RetrieveModelMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingPostSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
