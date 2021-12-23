from django_filters import rest_framework as filters

from .models import Room


class RoomFilter(filters.FilterSet):
    datetime_from = filters.IsoDateTimeFilter(method='filter_datetime_from')
    datetime_to = filters.IsoDateTimeFilter(method='filter_datetime_to')


    class Meta:
        model = Room
        fields = ['datetime_from', 'datetime_to']
