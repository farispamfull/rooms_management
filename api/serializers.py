import datetime

from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Booking, Room
from .validators import datetime_validator


class BookingPostSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(queryset=Room.objects.all(),
                                        slug_field='name')
    user = UserSerializer(read_only=True)
    booked_from_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                     validators=[
                                                         datetime_validator])
    booked_to_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                   validators=[
                                                       datetime_validator])

    def validate(self, attrs):
        print(attrs)
        one_hour = datetime.timedelta(hours=1)
        from_time = attrs.get('booked_from_datetime')
        to_time = attrs.get('booked_to_datetime')
        room = attrs.get('room')

        if to_time - from_time < one_hour:
            raise serializers.ValidationError(
                'бронировать нельзя меньше, чем на час')

        bookings = room.booking.exclude(
            booked_to_datetime__gt=to_time
        ).exclude(
            booked_from_datetime__lt=from_time,
        )

        if bookings.exists():
            raise serializers.ValidationError(
                'Выброное время уже занято'
            )


        return attrs

    class Meta:
        model = Booking
        fields = (
            'id', 'booked_from_datetime', 'booked_to_datetime', 'user', 'room')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('booked_from_datetime', 'booked_to_datetime', 'user')


class RoomSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(many=True)

    class Meta:
        model = Room
        fields = ('name', 'description', 'booking')
