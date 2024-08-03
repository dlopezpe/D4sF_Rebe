# aplicacion/settings/common.py

from decouple import config

from utils.obtain_format_date import obtain_format_date as od
from .base import *

# Url sentinel
url_api_instances = config('URL_API_SENTINEL_INSTANCES')
url_api_wms = config('URL_API_SENTINEL_WMS')
url_api_token = config('URL_API_SENTINEL_TOKEN')
url_api_id = config('CLIENT_ID')
url_api_secret = config('CLIENT_SECRET')
url_api_data_products_1242 = config('URL_API_SENTINEL_DATA_PRODUCTS_1242')
url_api_data_products_647 = config('URL_API_SENTINEL_DATA_PRODUCTS_647')
url_api_data_sets: object = config('URL_API_SENTINEL_DATA_SETS')
url_api_data_source = config('URL_API_SENTINEL_DATA_SOURCE')

url_api_false_layers = config('FALSE_LAYERS_')
url_api_crs = config('CRS_')
url_api_time = config('TIME_')
url_api_eval_script = config('EVAL_SCRIPT')



# Logging app

log_file = config('LOG_FILENAME')

filename = log_file + str(od.year_eng()) + '.log'
log_level = config('LOG_LEVEL')
max_log_size_bytes = int(config('MAX_LOG_SIZE_BYTES'))
backup_count = config('BACKUP_COUNT')
encoding = config('ENCODING')
django_log_level = config("DJANGO_LOG_LEVEL", default="INFO")

# LOGGING

# Determina la ruta del LOG dependiendo del sistema operativo
if platform.system() == 'Windows':
    LOG_DIR = os.path.join(BASE_DIR, 'logs\\')

    # String que deseas eliminar
    string_a_eliminar = "\\backend"
elif platform.system() == 'Linux':
    LOG_DIR = os.path.join(BASE_DIR, 'logs/')

    # String que deseas eliminar
    string_a_eliminar = "/backend"



# Eliminar el string de la cadena
LOG_DIR = LOG_DIR.replace(string_a_eliminar, "")

LOG_FILE = filename
LOG_PATH = LOG_DIR + LOG_FILE

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(LOG_PATH):
    f = open(LOG_PATH, 'a').close()  # create empty log file
else:
    f = open(LOG_PATH, "w").close()  # clear log file

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s]  %(module)s %(process)d %(thread)d - %(message)s'
        },
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(module)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': log_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH,
            'maxBytes': max_log_size_bytes,
            'backupCount': backup_count,
            'encoding': encoding,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': log_level,
            'propagate': True,
        },
    },
}

# Django Backend
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'rest_framework_gis',
    'django.contrib.gis',
    'corsheaders',
    'modulos.employees',
    'modulos.roles',
    'modulos.groups',
    'modulos.parcelas',
    'modulos.user',
    'modulos.profiles',
    'modulos.enterprises',
    'modulos.imgprocess',
    'modulos.cooperatives',
    'modulos.newimgprocess',
    'modulos.campanas',
    'modulos.trazas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # username
    'backend.get_username.RequestMiddleware'
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CORS_ORIGIN_ALLOW_ALL = True
WSGI_APPLICATION = 'backend.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
MEDIA_URL = '/media/'
STATIC_ROOT = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/parcels')

# Default primary key field type
# https://docs.djangoproject.com/en/3.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
