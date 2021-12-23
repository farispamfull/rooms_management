from rest_framework import serializers

from api.models import Booking
from .models import User


# обход циклического импорта
class BookingSerializer(serializers.ModelSerializer):
    booked_from_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                     read_only=True)
    booked_to_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                   read_only=True)
    room = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Booking
        fields = ('id', 'room', 'booked_from_datetime', 'booked_to_datetime',)


class UserSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(many=True, read_only=True)

    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'email', 'phone', 'booking')
        model = User
