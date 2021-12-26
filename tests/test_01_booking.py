from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone

from .common import create_booking, create_users_api, auth_client, create_rooms


class Test01BookingAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_booking_get_not_auth(self, client):
        response = client.get('/api/v1/booking/')
        assert response.status_code != 404, (
            'Страница `/api/v1/booking/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/v1/booking/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_booking_get_auth(self, user_client):
        user = create_users_api(user_client)
        client_user = auth_client(user)
        response = client_user.get('/api/v1/booking/')

        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/v1/booking/` c токена авторизации обычного юзера вовращается  статус 403'
        )
        response = user_client.get('/api/v1/booking/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/booking/` c токена авторизации staff юзера вовращается  статус 200'
        )
        rooms, booking, times = create_booking(user_client)
        response = user_client.get('/api/v1/booking/')
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/v1/booking/` возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/v1/booking/` возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/v1/booking/` возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/v1/booking/` возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 2, (
            'Проверьте, что при GET запросе `/api/v1/booking/` возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/v1/booking/` возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
        assert len(data['results']) == 2 and data['results'][0].get(
            'booked_from_datetime') in booking[0]['booked_from_datetime'] \
               and data['results'][1].get('booked_from_datetime') in \
               booking[1]['booked_from_datetime'], (
            'Проверьте, что при GET запросе `/api/v1/booking/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_booking_post_not_auth(self, client, user_client):
        create_rooms(user_client)
        data = {
            'some': 55,
        }
        response = client.post('/api/v1/booking/', data=data)
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе `/api/v1/booking/` без токена авторизации'
            ' возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_booking_post_auth(self, client, user_client, admin):
        rooms = create_rooms(user_client)
        data = {
        }
        response = user_client.post('/api/v1/booking/', data=data)

        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c не правильными'
            ' данными возвращается статус 400'
        )
        data = {
            'booked_from_datetime': '2021',
            'booked_to_datetime': '2021',
            'room': rooms[0]['name']
        }

        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c не правильными'
            ' данными возвращается статус 400'
        )
        data = {
            'booked_from_datetime': self.replace_time(
                timezone.now() - timedelta(hours=3)),
            'booked_to_datetime': self.replace_time(
                timezone.now() - timedelta(hours=1)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c не правильными'
            ' данными возвращается статус 400.'
            ' Нельзя сделать бронирование на прошедшее время'
        )
        data = {
            'booked_from_datetime': self.replace_time(
                timezone.now() - timedelta(hours=1)),
            'booked_to_datetime': self.replace_time(
                timezone.now() + timedelta(hours=1)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c не правильными'
            ' данными возвращается статус 400.'
            ' Нельзя сделать бронирование на прошедшее время'
        )
        data = {
            'booked_from_datetime': self.replace_time(
                timezone.now() + timedelta(hours=1)),
            'booked_to_datetime': self.replace_time(
                timezone.now() - timedelta(hours=1)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c не правильными'
            ' данными возвращается статус 400.'
            ' Нельзя сделать бронирование на прошедшее время'
        )

        min_time = getattr(settings, 'MIN_ROOM_TIME', timedelta(hours=1))
        data = {
            'booked_from_datetime': self.replace_time(
                timezone.now() + min_time),
            'booked_to_datetime': self.replace_time(
                timezone.now() + min_time),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c не правильными '
            'данными возвращается статус 400. '
            f'Нельзя сделать бронирование на промежуток меньше, чем {str(min_time)}'
        )

        max_time = getattr(settings, 'MAX_ROOM_TIME', timedelta(hours=4))
        data = {
            'booked_from_datetime': self.replace_time(
                timezone.now() + timedelta(minutes=10)),
            'booked_to_datetime': self.replace_time(
                timezone.now() + max_time + timedelta(hours=1)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c не правильными '
            'данными возвращается статус 400. '
            f'Нельзя сделать бронирование на промежуток больше, чем {str(max_time)}'
        )
        min_time = getattr(settings, 'MIN_ROOM_TIME', timedelta(hours=1))
        data = {
            'booked_from_datetime': self.replace_time(
                timezone.now() + timedelta(minutes=10)),
            'booked_to_datetime': self.replace_time(
                timezone.now() + min_time + min_time),
            'room': rooms[0]['name']
        }

        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c правильными '
            'данными возвращается статус 201. '
        )
        response_data = response.json()

        assert type(response_data.get('id')) is int, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c правильными '
            'данными возвращается id  '
        )
        assert response_data.get('booked_from_datetime') in data[
            'booked_from_datetime'], (
            'Проверьте, что при POST запросе `/api/v1/booking/` c правильными '
            'данными возвращается booked_from_datetime  '
        )
        assert response_data.get('booked_to_datetime') in data[
            'booked_to_datetime'], (
            'Проверьте, что при POST запросе `/api/v1/booking/` c правильными '
            'данными возвращается booked_from_datetime  '
        )

        assert response_data.get('room') == rooms[0]['name'], (
            'Проверьте, что при POST запросе `/api/v1/booking/` c правильными '
            'данными возвращается room '
        )
        assert response_data.get('user') == admin.email, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c правильными '
            'данными возвращается user '
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_booking_get_id(self, user_client, client):
        rooms, booking, times = create_booking(user_client)
        user = create_users_api(user_client)
        client_user = auth_client(user)

        response = client.get(f'/api/v1/booking/{booking[0]["id"]}/')
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/v1/booking/id/` без токена авторизации'
            ' возвращается статус 401'
        )
        response = client_user.get(f'/api/v1/booking/{booking[0]["id"]}/')

        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/v1/booking/{id/` c токен авторизации'
            ' не автора возвращается статус 403'
        )

        response = user_client.get(f'/api/v1/booking/{booking[0]["id"]}/')
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе `/api/v1/booking/id/` c токен авторизации'
            ' админа возвращается статус 200'
        )
        data = {
            'booked_from_datetime': self.replace_time(
                timezone.now() + timedelta(hours=5)),
            'booked_to_datetime': self.replace_time(
                timezone.now() + timedelta(hours=6)),
            'room': rooms[0]['name']
        }
        pre_response = client_user.post('/api/v1/booking/', data=data)
        booking_id = pre_response.json()['id']

        response = client_user.get(f'/api/v1/booking/{booking_id}/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/booking/4/` c токен авторизации'
            ' автора возвращается статус 200'
        )
        response = user_client.get(f'/api/v1/booking/{booking_id}/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/booking/4/` c токен авторизации'
            ' админ может посмотреть любой booking'
        )

        response_data = response.json()
        assert response_data.get('id') == booking_id, (
            'Проверьте, что при POST запросе `/api/v1/booking/4/` c правильными '
            'данными возвращается id '
        )
        assert response_data.get('booked_from_datetime') in data[
            'booked_from_datetime'], (
            'Проверьте, что при POST запросе `/api/v1/booking/4/` c правильными '
            'данными возвращается booked_from_datetime  '
        )
        assert response_data.get('booked_to_datetime') in data[
            'booked_to_datetime'], (
            'Проверьте, что при POST запросе `/api/v1/booking/4/` c правильными '
            'данными возвращается booked_from_datetime  '
        )
        assert response_data.get('room') == data['room'], (
            'Проверьте, что при POST запросе `/api/v1/booking/4/` c правильными '
            'данными возвращается room '
        )
        assert response_data.get('user') == user.email, (
            'Проверьте, что при POST запросе `/api/v1/booking/4/` c правильными '
            'данными возвращается user '
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_booking_post_validate_logic(self, user_client):
        rooms, booking, times = create_booking(user_client)
        time_to = times[0]['time_to']
        time_from = times[0]['time_from']
        data = {
            'booked_from_datetime': self.replace_time(
                time_from + timedelta(minutes=30)),
            'booked_to_datetime': self.replace_time(
                time_to - timedelta(minutes=30)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c временем, которое уже занято'
            ' возвращается статус 400 '
        )
        data = {
            'booked_from_datetime': self.replace_time(
                time_from + timedelta(minutes=30)),
            'booked_to_datetime': self.replace_time(
                time_to + timedelta(minutes=30)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c временем, которое уже занято'
            ' возвращается статус 400 '
        )
        data = {
            'booked_from_datetime': self.replace_time(
                time_from - timedelta(minutes=30)),
            'booked_to_datetime': self.replace_time(
                time_to - timedelta(minutes=30)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c временем, которое уже занято'
            ' возвращается статус 400 '
        )
        data = {
            'booked_from_datetime': self.replace_time(
                time_from - timedelta(minutes=30)),
            'booked_to_datetime': self.replace_time(
                time_to + timedelta(minutes=30)),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c временем, которое уже занято'
            ' возвращается статус 400 '
        )
        data = {
            'booked_from_datetime': self.replace_time(
                time_from),
            'booked_to_datetime': self.replace_time(
                time_to),
            'room': rooms[0]['name']
        }
        response = user_client.post('/api/v1/booking/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/booking/` c временем, которое уже занято'
            ' возвращается статус 400 '
        )

    def replace_time(self, time):
        return str(time.replace(microsecond=0, second=0))

    @pytest.mark.django_db(transaction=True)
    def test_07_booking_filter(self, user_client):
        """
        Рассматриваем фильтрацию rooms по отрезкам времени booking
        Рассматриваем все случаи пересечения с отрезком времени.
        """
        rooms, booking, times = create_booking(user_client)

        datetime_from = self.replace_time(
            times[0]['time_from'] + timedelta(minutes=30))
        datetime_to = self.replace_time(
            times[0]['time_to'] - timedelta(minutes=30))

        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_to}&datetime_from={datetime_from}')

        data = response.data
        assert data['count'] == 1, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
        assert data['results'][0]['id'] == rooms[1]['id'], (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )

        datetime_from = self.replace_time(
            times[0]['time_from'] - timedelta(hours=1))
        datetime_to = self.replace_time(
            times[0]['time_from'])
        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_to}&datetime_from={datetime_from}')

        data = response.data
        assert data['count'] == 2, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
        datetime_from = self.replace_time(
            times[0]['time_to'] + timedelta(minutes=30))
        datetime_to = self.replace_time(
            times[0]['time_to'] + timedelta(hours=1, minutes=30))

        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_to}&datetime_from={datetime_from}')
        data = response.data

        assert data['count'] == 2, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )

        datetime_from = self.replace_time(
            times[0]['time_to'])
        datetime_to = self.replace_time(
            times[0]['time_to'] + timedelta(hours=1))

        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_from}&datetime_from={datetime_to}')
        data = response.data

        assert data['count'] == 2, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
        datetime_from = self.replace_time(
            times[0]['time_from'] + timedelta(hours=1))
        datetime_to = self.replace_time(
            times[0]['time_to'] + timedelta(hours=1))

        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_to}&datetime_from={datetime_from}')

        data = response.data

        assert data['count'] == 1, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
        assert data['results'][0]['id'] == rooms[1]['id'], (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )

        datetime_from = self.replace_time(
            times[0]['time_from'] - timedelta(hours=1))
        datetime_to = self.replace_time(
            times[0]['time_to'] - timedelta(hours=1))

        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_to}&datetime_from={datetime_from}')

        data = response.data

        assert data['count'] == 1, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
        assert data['results'][0]['id'] == rooms[1]['id'], (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )

        datetime_from = self.replace_time(
            times[0]['time_from'])
        datetime_to = self.replace_time(
            times[0]['time_to'])

        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_to}&datetime_from={datetime_from}')

        data = response.data

        assert data['count'] == 1, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
        assert data['results'][0]['id'] == rooms[1]['id'], (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
        datetime_from = self.replace_time(
            times[0]['time_from'] - timedelta(hours=1))

        datetime_to = self.replace_time(
            times[0]['time_to'] + timedelta(hours=1))

        response = user_client.get(
            f'/api/v1/rooms/?datetime_to={datetime_to}&datetime_from={datetime_from}')

        data = response.data

        assert data['count'] == 1, (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно. '

        )
        assert data['results'][0]['id'] == rooms[1]['id'], (
            'Проверьте, что при GET запросе к api/v1/rooms/ фильтрация по datetime_to'
            ' datetime_from работает правильно'
        )
