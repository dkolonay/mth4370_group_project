#!/bin/sh
set -e

until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
    sleep 1
done

python manage.py migrate --noinput

exec "$@"