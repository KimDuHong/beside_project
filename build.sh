#!/bin/sh 

echo "==> Migration 파일 생성"
yes | python manage.py makemigrations

echo "==> Migrate 실행"
python manage.py migrate 

echo "==> collect static 실행"
python manage.py collectstatic

echo "==> 배포!"
# gunicorn --bind 0.0.0.0:8000 config.wsgi:application