# rooms_management
[![CI](https://github.com/farispamfull/rooms_management/actions/workflows/rooms_management.yml/badge.svg)](https://github.com/farispamfull/rooms_management/actions/workflows/rooms_management.yml)
* [Техническое задание](#tech-task)
* [Описание проекта](#description)
* [Процесс регистрации](#registations)
* [API](#api)
* [Локальный запуск](#dev)

Приложение: http://3.124.145.142/api/v1

## Техническое задание <a name="tech-task"></a>

Необходимо реализовать веб-сервис с помощью Django и захостить на сервере (на каком удобно, например, heroku). 

Готовым ответом будет являться url развернутого приложения и исходники в архиве, либо ссылка на публичный git репозиторий. Необходимо выгрузить перечень используемых сторонних библиотек в файл requirements.txt и сохранить его в папке с проектом.

Сервис должен предоставлять REST API, позволяющее осуществлять бронирование рабочих мест в кабинетах. API должно предоставлять ресурсы для:
* Бронирования рабочих мест на заданный период времени;

* Просмотра списка бронирований по id рабочего места;

* Авторизации пользователя любым методом (Basic Auth годится);

* Ресурс рабочих мест должен иметь 2 необязательных параметра фильтрации: «datetime_from», «datetime_to», ожидающих datetime в формате ISO. Если данные валидны, то ответом на GET с указанными параметрами должен быть список рабочих мест, свободных в указанный временной промежуток.


## Описание проекта <a name="description"></a>

* В проекте есть два основых пути для взаимодействия: `api/v1/booking/` и `api/v1/rooms/`

* У комнат при запросе выводится только актуальное бронирование на текущий момент времени
 
* Рассмотрены узкие моменты:
  - пользователь не может бронировать больше или меньше определенного времени
  - бронировать можно только на свободное время
  - нет вывода старых бронирований
  - бронировать можно только на будущие даты

* Есть эндпоинт для users `api/v1/users/`. Доступен только для staff:
  - позволяет staff видеть брони каждого юзера
  - есть фильтр по конкретной брони, чтобы узнать юзера.
  - свои данные и все бронирования можно посмотреть на `api/v1/users/me` (permissions: authentication)

 

* Ключевой момент тестового задания - фильтрация комнат по времени - написан с использованием свойств пересечений множеств



## Процесс регистрации <a name="registations"></a>
1. Пользователь отправляет post запрос с параметрами  `email`,`username`,`password`, 
`first_name`,`last_name`,`phone` на `/api/v1/auth/signup/`.

3. Далее пользователь отправляет post запрос с параметрами  `email`, `password` на `/api/v1/auth/token/login/`.
В ответ ему приходит **токен** 

* При желании юзер может посмотреть свои данные на `/api/v1/users/me/`
* Для выхода из системы get запрос на `api/v1/auth/token/logout/`


## API
```
Prefix /api/v1/

users/
  - get (permissions: staff)
  - filter: booking(id)

users/:id/
  - get (permissions: staff)
  - delete (permissions: staff)

users/me/
  - get (permissions: authentication)

booking/
  - post 
    - комната указывается по name
  - delete (permissions: owner or staff)
  - patch (permissions: owner or staff)

rooms/
  - post (permissions: staff)
  - get (permissions: authentication)
  - delete (permissions: staff)

  -  filter: datetime_from & datetime_to


```



```
Prefix /api/v1/auth/

token/login/
  - post

token/logout/
  - get



```

## Локальный запуск Docker <a name="dev"></a>
Создайте файл .env и поместите в корневой каталог проекта

Запишите в нем переменные окружения:
```
DEBUG=False
SECRET_KEY=Сгенерируйте ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgresql
POSTGRES_USER=postgresql
POSTGRES_PASSWORD=postgresql
DB_HOST=db
DB_PORT=5432
```
запустите docker-compose:
```
 docker-compose -f docker-compose.yaml -f docker-compose-dev.yaml up -d
```

При первом запуске выполнить миграции:

```
docker-compose exec web python manage.py makemigration
docker-compose exec web python manage.py migrate
```

Соберите статику:
```
docker-compose exec web python manage.py collectstatic --no-input