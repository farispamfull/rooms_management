from django_filters import rest_framework as filters

from users.models import User


class UsersFilter(filters.FilterSet):
    booking = filters.NumberFilter(method='filter_booking')
    room = filters.CharFilter(method='filter_room')

    def filter_booking(self, queryset, name, value):
        return queryset.filter(booking__id=value)

    def filter_booking(self, queryset, name, value):
        return queryset.filter(booking__room__name=value)

    class Meta:
        model = User
        fields = ['booking', 'room']
