# aplicacion/settings/produccion.py

from decouple import config, Csv
import os

from django.core.exceptions import ImproperlyConfigured

# Configuracion específica para produccion
# Django Backend

# SECURITY WARNING: keep the secret key used in prod secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY variable is not set")

from datetime import timedelta

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
}

# SECURITY WARNING: don't run with debug turned on in prod!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', default='', cast=Csv())

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = config('STATIC_URL')
PARCEL_FOLDER = config('PARCEL_FOLDER')
SHAPES_FOLDER = config('SHAPES_FOLDER')
CAMPANA_FOLDER = config('CAMPANA_FOLDER')
SITE_URL = config('SITE_URL')

# PostgreSQL with PostGis
if not all(
        [os.getenv('DB_DRIVER'), os.getenv('POSTGRES_DB'), os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'),
         os.getenv('POSTGRES_HOST'),os.getenv('POSTGRES_PORT')]):
    raise ImproperlyConfigured('Database configuration is incomplete.')

DATABASES = {
    'default': {
        # Este es el motor de base de datos que se utiliza cuando necesitas capacidades espaciales en
        # tu aplicacion Django
        'ENGINE': config('DB_DRIVER', default='django.contrib.gis.db.backends.postgis'),
        'NAME': config('POSTGRES_DB', default='dataforsmartfarming'),
        'USER': config('POSTGRES_USER', default='dataforsmartfarmingbackend'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='Cm&O8nOlKZlb'),
        # uses the container if set, otherwise it runs locally
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ENABLED_EMAIL = config('ENABLED_EMAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = config('LANGUAGE_CODE')
TIME_ZONE = config('TIME_ZONE')
USE_I18N = config('USE_I18N')
USE_L10N = config('USE_L10N')
USE_TZ = config('USE_TZ')
