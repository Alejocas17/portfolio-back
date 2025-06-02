#!/bin/sh
echo "Waiting for PostgreSQL..."
until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"; do
  sleep 1
done
echo "PostgreSQL is ready!"
python manage.py makemigrations
python manage.py migrate
exec "$@"