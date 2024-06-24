
import os
import re
import datetime
from collections import defaultdict
import sqlite3
from monitor.settings import DATABASES

def obtener_fecha(is_start_date=False):
    while True:
        try:
            fecha_str = input("Por favor, introduce una fecha en formato YYYY-MM-DD: ")
            # añadir la hora y los minutos a la fecha
            hour = " 00:00:00" if is_start_date else " 23:59:59"
            fecha_full = fecha_str + hour
            fecha = datetime.datetime.strptime(fecha_full, "%Y-%m-%d %H:%M:%S")
            return fecha
        except ValueError:
            print("Formato de fecha incorrecto. Asegúrate de usar el formato correcto (YYYY-MM-DD).")



def tiene_extension_png(texto):
    return re.search(r"\.png$", texto) is not None


def contar_archivos_por_extension_y_fecha(path):
    # Crear diccionarios para almacenar la cuenta por extensión y por fecha
    extension_count = defaultdict(int)
    fecha_count = defaultdict(int)

    # Recorrer todos los archivos en el directorio
    for root, _, files in os.walk(path):
        for filename in files:
            # Obtener la extensión del archivo
            _, ext = os.path.splitext(filename)
            ext = ext.lower()  # Convertir la extensión a minúsculas para la consistencia

            # Obtener la fecha de creación del archivo
            filepath = os.path.join(root, filename)
            fecha_creacion = datetime.datetime.fromtimestamp(os.path.getctime(filepath)).date()

            # Actualizar las cuentas
            extension_count[ext] += 1
            fecha_count[fecha_creacion] += 1

    # Imprimir los resultados
    print("Archivos por extensión:")
    for ext, count in extension_count.items():
        print(f"{ext}: {count} archivos")

    print("\nArchivos por fecha de creación:")
    for fecha, count in fecha_count.items():
        print(f"{fecha}: {count} archivos")




def eliminar_archivos(path, extensiones, fecha_inicio, fecha_fin):
    archivos_eliminados = 0
    # Obtener la lista de archivos en el directorio
    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Verificar la extensión del archivo
            if file_path.endswith(tuple(extensiones)):
                try:
                    # Obtener la fecha de modificación del archivo
                    fecha_modificacion = datetime.datetime.fromtimestamp(
                        os.path.getmtime(file_path)
                    )
                    
                    
                    # Verificar si la fecha de modificación está en el rango especificado
                    if fecha_inicio <= fecha_modificacion <= fecha_fin:
                        print(f"Nombre del archivo: {filename}")
                        print(f"Fecha de modificación: {fecha_modificacion}")
                        archivos_eliminados += 1
                        #os.remove(file_path)
                        is_png_file = tiene_extension_png(filename)
                        if is_png_file:
                            full_name = 'media/parcels/'+ filename
                            eliminar_registro_por_nombre(full_name)
                except Exception as e:
                    print(f"Error al eliminar {file_path}: {str(e)}")

    return archivos_eliminados

def eliminar_registro_por_nombre(nombre):
    try:
        path_db = DATABASES['default']['NAME']
        # Conectarse a la base de datos SQLite
        conexion = sqlite3.connect(path_db)
        cursor = conexion.cursor()

        # Verificar si el registro existe en la primera tabla
        consulta1 = f"SELECT id FROM ndvimonitor_ndvimonitor WHERE image = '{nombre}'"
        #print(consulta1)
        cursor.execute(consulta1)
        resultado1 = cursor.fetchone()

        # Verificar si el registro existe en la segunda tabla
        consulta2 = f"SELECT id FROM moisturemonitor_moisturemonitor WHERE image = '{nombre}'"
        #print(consulta2)
        cursor.execute(consulta2)
        resultado2 = cursor.fetchone()

        

        if resultado1 or resultado2:
            # Obtener la fecha y hora actual
            fecha_hora_actual = datetime.now()
            # Si se encuentra en alguna de las tablas, eliminar el registro
            if resultado1:
                cursor.execute("INSERT INTO ndvimonitor_ndvimonitor (deleted) VALUES (?) WHERE image = '?'", (fecha_hora_actual,nombre,))
            if resultado2:
                cursor.execute("INSERT INTO moisturemonitor_moisturemonitor (deleted) VALUES (?) WHERE image = '?'", (fecha_hora_actual,nombre,))

            # Confirmar los cambios
            conexion.commit()
            print(f"Registro con nombre '{nombre}' modificado con éxito.")
        
    except sqlite3.Error as error:
        # En caso de error, hacer un rollback para deshacer cualquier cambio pendiente
        conexion.rollback()
        print("Error al eliminar el registro:", error)

    finally:
        # Cerrar la conexión a la base de datos
        conexion.close()




if __name__ == "__main__":
    
    path = "./media/parcels" # Cambia esto al directorio deseado
    extensiones = (".xlsx",".png")  # Cambia las extensiones deseadas

    
    contar_archivos_por_extension_y_fecha(path)
    
    print("Introduce la fecha de inicio:")
    is_fecha_inicio = True
    fecha_inicio = obtener_fecha(is_fecha_inicio)

    print("Introduce la fecha final:")
    fecha_final = obtener_fecha()

    print("Fecha de inicio:", fecha_inicio)
    print("Fecha final:", fecha_final)
    
    

    confirmacion = input("¿Deseas eliminar los archivos? (si/no): ")
    if confirmacion.lower() == "si":
        print(f"Eliminando archivos del path: {path}")
        archivos_eliminados = eliminar_archivos(path, extensiones, fecha_inicio, fecha_final)
        print(f"Total de archivos eliminados: {archivos_eliminados}")
    else:
        print("Operación cancelada.") 
     
    

    
