from django_filters import rest_framework as filters

from .models import Booking


class BookingFilter(filters.FilterSet):
    user = filters.NumberFilter(field_name='user__id')
    room = filters.CharFilter(field_name='room__name', lookup_expr='iexact')
    date_gte = filters.DateFilter(field_name='booked_from_datetime',
                                  lookup_expr='gte')
    date_lte = filters.DateFilter(field_name='booked_to_datetime',
                                  lookup_expr='lte')

    class Meta:
        model = Booking
        fields = ['user', 'room', 'date_gte', 'date_lte']
