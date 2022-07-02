#!/bin/sh

set -e

./wait-for-it.sh -t 60 db:5432
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi