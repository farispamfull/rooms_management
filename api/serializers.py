from django.conf import settings
from rest_framework import serializers

from .models import Booking, Room
from .validators import datetime_validator


class BookingPostSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(queryset=Room.objects.all(),
                                        slug_field='name')
    user = serializers.SlugRelatedField(
        slug_field='email', read_only=True)
    booked_from_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                     validators=[
                                                         datetime_validator])
    booked_to_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                   validators=[
                                                       datetime_validator])

    def validate(self, attrs):
        from_time = attrs.get('booked_from_datetime')
        to_time = attrs.get('booked_to_datetime')
        room = attrs.get('room')
        current_time = to_time - from_time

        if current_time < settings.MIN_ROOM_TIME:
            raise serializers.ValidationError(
                'Слишком маленький промежуток времени')
        if current_time > settings.MAX_ROOM_TIME:
            raise serializers.ValidationError(
                'Слишком большой промежуток времени')

        bookings = room.booking.filter(
            booked_from_datetime__lt=to_time,
            booked_to_datetime__gt=from_time)

        if bookings.exists():
            raise serializers.ValidationError(
                'выбранное  время уже занято'
            )

        return attrs

    class Meta:
        model = Booking
        fields = (
            'id', 'booked_from_datetime', 'booked_to_datetime', 'user', 'room')


class BookingSerializer(serializers.ModelSerializer):
    booked_from_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                     read_only=True)
    booked_to_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M',
                                                   read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'booked_from_datetime', 'booked_to_datetime',)
        read_only_fields = fields


class RoomSerializer(serializers.ModelSerializer):
    booking = serializers.SerializerMethodField(
        method_name='get_current_booking', read_only=True)

    def get_current_booking(self, obj):
        current_booking = obj.current_booking
        return BookingSerializer(current_booking, many=True).data

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'booking')


class DateSerialzier(serializers.Serializer):
    datetime_from = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    datetime_to = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
