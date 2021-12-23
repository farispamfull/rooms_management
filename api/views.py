from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from .models import Booking, Room
from .permissions import (AuthenticatedOrStaffPermission, AuthenticatedOrOwner)
from .serializers import (BookingPostSerializer, RoomSerializer,
                          DateSerialzier, BookingSerializer)


class BookingViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin,
                     RetrieveModelMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingPostSerializer

    permission_classes = [AuthenticatedOrOwner]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookingSerializer
        return BookingPostSerializer

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

            return Room.objects.prefetch_related('booking').exclude(
                booking__booked_from_datetime__lte=datetime_to,
                booking__booked_to_datetime__gte=datetime_from)

        return Room.objects.all()
