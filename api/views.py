from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from .models import Booking, Room
from .serializers import BookingPostSerializer, RoomSerializer, DateSerialzier


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


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]

    # filterset_class = RoomFilter

    def get_queryset(self):
        query = self.request.query_params
        serializer = DateSerialzier(data=query)
        if serializer.is_valid():
            datetime_from = serializer.data['datetime_from']
            datetime_to = serializer.data['datetime_to']

            return Room.objects.prefetch_related('booking').exclude(
                booking__booked_from_datetime__lte=datetime_to,
                booking__booked_to_datetime__gte=datetime_from)

        return Room.objects.all()
