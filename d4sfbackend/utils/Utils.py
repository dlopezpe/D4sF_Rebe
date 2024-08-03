import datetime
import logging
from decouple import config

from modulos.trazas.utils import savelog


# Timestamp en segundos (ejemplo: 1660264635)
# Convertir el timestamp en un objeto datetime
def convert_epoc_to_date(timestamp_milliseconds):

    if timestamp_milliseconds is not None:
        timestamp_seconds = int(timestamp_milliseconds) / 1000

        dt_object = datetime.datetime.fromtimestamp(timestamp_seconds)

        # Formatear la fecha como "dd-mm-yyyy"
        formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        logging.debug("Fecha formateada: %s", formatted_date)
        return formatted_date


# Get the current timestamp
def get_current_ts():
    return datetime.datetime.now()


log_purpuse = config('LOG_PURPUSE')


def save_log(message, request, extra_data):
    if log_purpuse and request:
        context_logs = {
            'user_email': request.user,
            'message': message,
            'status': 'success',
            'extra_data': extra_data
        }
        savelog(context_logs, request)
