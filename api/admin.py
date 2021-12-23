from django.contrib import admin

from .models import Booking, Room


@admin.register(Booking)
class BookingAdmim(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'room', 'booked_from_datetime',
        'booked_to_datetime'
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description'
    )
