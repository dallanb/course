#!/bin/sh

. ~/.bashrc

pip install -e .

if [ "$DATABASE" = "contest" ]; then
  echo "Waiting for PostgreSQL..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

gunicorn --bind 0.0.0.0:5000 manage:app
