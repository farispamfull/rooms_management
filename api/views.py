from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin)
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import BookingFilter
from .models import Booking, Room
from .permissions import (AuthenticatedOrStaffPermission, AuthenticatedOrOwner,
                          AuthenticatedOrAdmin)
from .serializers import (BookingPostSerializer, RoomSerializer,
                          DateSerialzier)


class ReadOnlyNotUpdateViewSet(ReadOnlyModelViewSet, DestroyModelMixin,
                               CreateModelMixin):
    pass


class BookingViewSet(ReadOnlyNotUpdateViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingPostSerializer
    permission_classes = [AuthenticatedOrAdmin, AuthenticatedOrOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AuthenticatedOrStaffPermission]

    def get_queryset(self):
        query = self.request.query_params
        serializer = DateSerialzier(data=query)
        if serializer.is_valid():
            datetime_from = serializer.data['datetime_from']
            datetime_to = serializer.data['datetime_to']

            filter_set = Booking.objects.filter(
                booked_from_datetime__lt=datetime_to,
                booked_to_datetime__gt=datetime_from)

            return Room.objects.prefetch_related('booking').exclude(
                booking__in=filter_set)

        return Room.objects.prefetch_related('booking')
