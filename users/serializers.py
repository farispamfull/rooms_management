from rest_framework import serializers


from .models import User


class UserSerializer(serializers.ModelSerializer):
    # booking = BookingSerializer(many=True, read_only=True)

    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'email', 'phone', 'booking')
        model = User
