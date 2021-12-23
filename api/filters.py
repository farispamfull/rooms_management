from django_filters import rest_framework as filters

from users.models import User


class UsersFilter(filters.FilterSet):
    booking = filters.NumberFilter(method='filter_booking')

    def filter_booking(self, queryset, name, value):
        return queryset.filter(booking__id=value)

    class Meta:
        model = User
        fields = ['booking']
