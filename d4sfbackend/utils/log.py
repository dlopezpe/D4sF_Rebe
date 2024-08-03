import logging
from logging.handlers import RotatingFileHandler
from utils.obtain_format_date import obtain_format_date as od

from ConfigParser import ConfigParser
from D4sfConstants import fichero_config_ini, seccion_log, log_file_const, \
    max_log_size_bytes_const, backup_count_const, encoding_const

# Configure logging to write to a file

config_parser_log = ConfigParser(fichero_config_ini)

log_file = config_parser_log.get_propiedad_value(seccion_log, log_file_const)
encoding = config_parser_log.get_propiedad_value(seccion_log, encoding_const)
max_log_size_bytes = config_parser_log.get_propiedad_value(seccion_log, max_log_size_bytes_const, "entero")
backup_count = config_parser_log.get_propiedad_value(seccion_log, backup_count_const, "entero")

filename = log_file+ str(od.year_eng())  +'.log'

# Configura el formato del registro
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Agrega el manejador al registrador raíz
root_logger = logging.getLogger()

# Configura el nivel de registro deseado (por ejemplo, DEBUG)
root_logger.setLevel(logging.DEBUG)

# Agrega el handler rotativo de ficheros
handler = logging.handlers.RotatingFileHandler(filename, maxBytes=max_log_size_bytes, backupCount=backup_count,
                                               encoding= encoding )

#handler = logging.FileHandler(filename, 'a', 'utf-8')
handler.setFormatter(formatter)

root_logger.addHandler(handler)

handler.close()