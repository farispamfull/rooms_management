FROM python:3.8.5

WORKDIR /code

COPY . .

RUN apt-get update -y && apt-get upgrade -y

RUN pip3 install -r requirements.txt

CMD gunicorn rooms_management.wsgi:application --bind 0.0.0.0:8000