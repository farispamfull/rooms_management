from django.contrib import admin

from .models import Booking, Room


@admin.register(Booking)
class BookingAdmim(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'room', 'booked_from_datetime',
        'booked_to_datetime'
    )
    search_fields = ('user__username', 'user__email')
    list_filter = ('room',)
    ordering = ['-booked_to_datetime']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'count_current_booking',
    )

    def count_current_booking(self, obj):
        return obj.current_booking.count()
