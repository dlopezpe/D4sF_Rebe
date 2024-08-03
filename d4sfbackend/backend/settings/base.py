# d4sfbackend/settings/base.py
# Configuracion base común a todos los entornos
import os
import platform

from decouple import config
from django.core.exceptions import ImproperlyConfigured

# Ruta del proyecto base

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar las variables de entorno desde el archivo .env
# Determina el entorno actual
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')


PYTHONPATH=os.getenv('PYTHONPATH', '/d4sfbackend')
if not PYTHONPATH:
    raise ImproperlyConfigured("PYTHONPATH variable is not set")

# Establece la ruta del archivo .env basado en el entorno actual o ruta del archivo .env
if ENVIRONMENT == "local":
    env_path = f"devops/{ENVIRONMENT}/.env"
else:
    env_path = f"devops/{ENVIRONMENT}/.env.{ENVIRONMENT}"

# Determina la ruta de GDAL dependiendo del sistema operativo
if platform.system() == 'Windows':
    gdal_path = 'C:\OSGeo4W'  # Reemplaza con la ruta correcta en Windows
elif platform.system() == 'Linux':
    gdal_path = '/usr/lib/libgdal.so'  # Reemplaza con la ruta correcta en Linux
else:
    raise Exception('Sistema operativo no soportado')


def set_environment(file, key, value):
    global env_lines, key_set
    # Lee las variables actuales en el archivo .env sin sobrescribir comentarios
    env_lines = []
    key_set = False
    if os.path.exists(env_path):
        with open(env_path, 'r') as file:
            env_lines = file.readlines()
            for i, line in enumerate(env_lines):
                if line.startswith(key):
                    env_lines[i] = f'{key}={value}\n'
                    key_set = True

    # Añade la variable GDAL_LIBRARY_PATH en este caso, si no estaba ya establecida
    if not key_set:
        env_lines.append(f'{key}={value}\n')

    # Escribe las variables actualizadas en el archivo .env
    with open(env_path, 'w') as file:
        file.writelines(env_lines)


set_environment(env_path, 'GDAL_LIBRARY_PATH', gdal_path)

# OSGeo4W for parcelas, el script detecta si estás en Windows (nt) o en otro sistema operativo como Linux/Unix/MacOS (posix)

OSGEO4W = config('GDAL_LIBRARY_PATH')
# Detectar el sistema operativo
if os.name == 'nt':  # Windows
    if '64' in platform.architecture()[0]:  # 64 bits
        OSGEO4W += "64"
    # No se necesita ajuste adicional para 32 bits en Windows

# No se necesita ajuste adicional para 32 bits ni 64 bits en sistemas POSIX
# Unix (incluyendo Linux) para platform.architecture()[0]="64" será libgdal.so y para la arquitectura 32 será opcional libgdal.so.1


os.environ['OSGEO4W_ROOT'] = OSGEO4W
os.environ['GDAL_DATA'] = OSGEO4W + r"\share\epsg_csv"
os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

# Django Backend
AUTH_USER_MODEL = 'user.User'
