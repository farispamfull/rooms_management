from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    @property
    def current_booking(self):
        return self.booking.filter(
            booked_from_datetime__gte=datetime.now(tz=None))

    def __str__(self):
        return self.name


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             related_name='booking')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='booking')
    booked_from_datetime = models.DateTimeField()
    booked_to_datetime = models.DateTimeField()
