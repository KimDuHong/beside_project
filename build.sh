#!/bin/bash

echo "==> Migration 파일 생성"
yes | python manage.py makemigrations

echo "==> Migrate 실행"
python manage.py migrate 

echo "==> 배포!"

if [[ "$SERVER" == "DEV" ]]
then
    echo "Deploy Gunicorn"
    echo "==> collect static 실행"
    python manage.py collectstatic --noinput
    gunicorn config.wsgi:application --bind 0.0.0.0:8000
else
    echo "Deploy Runserver"
    python manage.py runserver 0.0.0.0:8000
fi