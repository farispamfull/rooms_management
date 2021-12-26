from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


def create_users_api(user_client):
    data = {
        'username': 'TestUser1234',
        'first_name': 'user',
        'last_name': 'user',
        'phone': '+79006485327',
        'password': 'TestUser101',
        'email': 'testuser@gmail.fake',
    }
    user_client.post('/api/v1/auth/signup/', data=data)
    user = get_user_model().objects.get(email=data['email'])
    return user


def auth_client(user):
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


def auth_client_by_token(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client


def create_rooms(user_client):
    result = []
    data = {
        'name': '001',
        'description': 'first',

    }
    response = user_client.post('/api/v1/rooms/', data=data)
    data['id'] = response.json()['id']
    result.append(data)

    data = {
        'name': '002',
        'description': 'second',
    }
    response = user_client.post('/api/v1/rooms/', data=data)
    data['id'] = response.json()['id']
    result.append(data)

    return result


def create_times():
    result = []
    time_from = (timezone.now() + timedelta(hours=1))
    time_to = time_from + timedelta(hours=3)
    time = {
        'time_to': time_to,
        'time_from': time_from,
    }
    result.append(time)

    time_from = (timezone.now() + timedelta(hours=6))
    time_to = time_from + timedelta(hours=3)
    time = {
        'time_to': time_to,
        'time_from': time_from,
    }
    result.append(time)

    return result


def create_booking(user_client):
    rooms = create_rooms(user_client)
    times = create_times()
    booking = []
    data = {
        'room': rooms[0]['name'],
        'booked_to_datetime': str(times[0]['time_to']),
        'booked_from_datetime': str(times[0]['time_from']),
    }

    response = user_client.post('/api/v1/booking/', data=data)
    data['id'] = response.json()['id']
    booking.append(data)

    data = {
        'room': rooms[1]['name'],
        'booked_to_datetime': str(times[1]['time_to']),
        'booked_from_datetime': str(times[1]['time_from']),
    }
    response = user_client.post('/api/v1/booking/', data=data)
    data['id'] = response.json()['id']
    booking.append(data)

    return rooms, booking, times
