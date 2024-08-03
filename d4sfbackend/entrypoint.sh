#!/bin/bash

# Espera a que el servicio PostGIS esté listo
/wait-for-it.sh postgres:5432 -- echo "PostGIS is up"

# Ejecuta el comando makemigrations
python manage.py makemigrations

# Continúa con el comando runserver u otros comandos de Django
python manage.py migrate
python manage.py createsuperuser --noinput
