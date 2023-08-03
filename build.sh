#!/bin/sh 

echo "==> Migration 파일 생성"
yes | python manage.py makemigrations

echo "==> Migrate 실행"
python manage.py migrate 

echo "==> collect static 실행"
python manage.py collectstatic --noinput

echo "==> 배포!"
source .env
if [[ "$SERVER" == True ]]; then
    gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
else
    python manage.py runserver 0.0.0.0:8000
# gunicorn --bind 0.0.0.0:8000 config.wsgi:application