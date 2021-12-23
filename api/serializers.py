from rest_framework import serializers

from .models import Booking, Room


class BookingPostSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(queryset=Room.objects.all(),
                                        slug_field='name')

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
