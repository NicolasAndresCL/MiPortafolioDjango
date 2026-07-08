#!/bin/sh
# Aplica migraciones antes de arrancar el servidor y ejecuta el comando (gunicorn).
set -e

python manage.py migrate --noinput

exec "$@"
