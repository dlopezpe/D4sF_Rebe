# Dockerfile

# Utiliza una imagen base con Python y PostgreSQL
FROM python:3.8

# Instala las herramientas de desarrollo necesarias para compilar PostGIS, GDAL, logrotate, cron

RUN apt-get update && apt-get install -y \
        build-essential \
        postgresql-server-dev-all \
        libproj-dev \
        binutils \
        gdal-bin \
        libgdal-dev \
        logrotate \
        cron \
        libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*


#Actualizar paqueterias del PIP
RUN pip install --upgrade pip

# Copia el script de inicializacion de la base de datos
COPY initdb-postgis.sh /docker-entrypoint-initdb.d/

# Cambia los permisos del script de inicializacion de la base de datos para que sea ejecutable
RUN chmod +x /docker-entrypoint-initdb.d/initdb-postgis.sh

# Cambia el archivo de entrada por defecto para ejecutar el script de inicializacion de la base de datos antes de iniciar el servidor PostgreSQL
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf", "-c", "hba_file=/etc/postgresql/pg_hba.conf"]

# Continua con el resto de las configuraciones y comandos del Dockerfile

# Configurar el entorno
# Define la variable de entorno ENVIRONMENT (deberías proporcionar su valor al construir la imagen)
ARG ENVIRONMENT
ENV ENVIRONMENT=${ENVIRONMENT}

# Establece el directorio de trabajo en /d4sfbackend
WORKDIR /d4sfbackend

# Copia todo el contenido del directorio d4sfbackend al directorio de trabajo en el contenedor
COPY backend /d4sfbackend/backend
COPY manage.py  /d4sfbackend/
COPY requirements.txt  /d4sfbackend/

# Copia los archivos de configuracion según el entorno
COPY backend/settings/common.py /d4sfbackend/backend/settings/
COPY backend/settings/base.py /d4sfbackend/backend/settings/
COPY backend/settings/${ENVIRONMENT}.py /d4sfbackend/backend/settings/


# Copia los archivos de utilidades
COPY utils/ /d4sfbackend/utils/

# Copia los diferentes modulos que existan en d4sfbackend/*
COPY modulos /d4sfbackend/modulos/

# Establece la variable de entorno PYTHONPATH para incluir el directorio de tu proyecto
ENV PYTHONPATH "${PYTHONPATH}:/d4sfbackend"

# Copia el archivo .env.dev
COPY devops/${ENVIRONMENT}/ /d4sfbackend/

# Renombra el archivo .env.dev a .env
RUN mv /d4sfbackend/.env.${ENVIRONMENT} /d4sfbackend/.env

# Copia el archivo de configuracion de logrotate a la ubicacion correcta
COPY devops/logrotate/d4sfbackendlog.conf /etc/d4sfbackendlog.conf

# Copia el script de logrotate a /etc/cron.daily/
COPY devops/logrotate/logrotate-cron /etc/cron.daily/logrotate-cron

# Inicia el servicio cron
CMD ["cron", "-f"]

#Docker indica la configuracion del entorno para la ejecucion de aplicaciones Python dentro del contenedor.
#se desactiva este búfer, lo que significa que la salida se muestra inmediatamente en la consola a medida que se produce.
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala las dependencias de la aplicacion
RUN pip install --no-cache-dir -r requirements.txt

# Define la variable de entorno DJANGO_SETTINGS_MODULE en funcion de ENVIRONMENT
ENV DJANGO_SETTINGS_MODULE=backend.settings.${ENVIRONMENT}

# Copia el script de inicio
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copia wait-for-it.sh
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Ejecuta las migraciones y crea el superusuario (si es necesario)
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py createsuperuser --noinput

# Expone el puerto 8000 en el contenedor
EXPOSE 8000

# Ejecuta las migraciones y crea el superusuario (si es necesario) dependiendo del entorno
RUN if [ "$ENVIRONMENT" = "prod" ]; then \
        echo "Running in production environment"; \
    else \
        echo "Running non-production environment"; \
    fi

# Ejecuta el servidor de desarrollo de Django en entorno de desarrollo cuando el contenedor se inicia
CMD ["sh", "-c", "if [ \"$ENVIRONMENT\" = \"prod\" ]; then gunicorn aplicacion.wsgi:application -b 0.0.0.0:8000; \
else \
python manage.py runserver 0.0.0.0:8000; fi"]



