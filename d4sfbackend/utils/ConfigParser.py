import configparser
import logging


class ConfigParser:

    def __init__(self, config_file_parser):
        # Cargar el archivo de propiedades
        self.config = configparser.ConfigParser()
        self.config.read(config_file_parser)

    # Obtener y mostrar las propiedades actuales
    def get_propiedad_value(self, seccion, key, type_propiedad=None):
        if type_propiedad == "entero":
            value = self.config.getint(seccion, key)
        elif type_propiedad == "boolean":
            value = self.config.getboolean(seccion, key)
        elif type_propiedad == "float":
            value = self.config.getfloat(seccion, key)
        else:
            value = self.config.get(seccion, key)

        logging.info("El valor de la propiedad es %s para la key [%s] del fichero de properties", value, key )
        return value

    # Modificar una propiedad en tiempo de ejecución
    def set_propiedad_value(self, seccion, key, value):
        self.config.set(seccion, key, value)
        logging.info("El nuevo valor de la propiedad es %s para la key [%s] del fichero de properties", value, key)
        # Guardar los cambios en el archivo de propiedades
        with open(seccion, 'w') as configfile:
            self.config.write(configfile)

        self.read_propiedades(seccion)

    # Volver a cargar el archivo para obtener las propiedades actualizadas
    def read_propiedades(self, seccion):
        self.config.read(seccion)