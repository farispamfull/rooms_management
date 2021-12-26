import datetime

import phonenumbers
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

now = timezone.now()


def datetime_validator(value):
    if value.replace(tzinfo=None) < datetime.datetime.now():
        raise serializers.ValidationError('Указана прошедшая дата')
    return value


def phone_validator(value):
    region = getattr(settings, 'PHONE_REGION', 'RU')
    phone_number = phonenumbers.parse(value, region)
    if not phonenumbers.is_valid_number(phone_number):
        raise serializers.ValidationError(
            'Проверьте, что правильно ввели номер телефона')
    return value
