import datetime

from django.utils import timezone
from rest_framework import serializers

now = timezone.now()


def datetime_validator(value):
    if value.replace(tzinfo=None) < datetime.datetime.now():
        raise serializers.ValidationError('Указана прошедшая дата')
    return value
