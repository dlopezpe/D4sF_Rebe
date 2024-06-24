import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import uuid
import urllib.request

nombreArchivo = str(uuid.uuid1().int)+'.png'
urllib.request.urlretrieve("https://services.sentinel-hub.com/ogc/wms/13e7a2a7-2e3e-489e-8a65-eb971dab81af?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS=NDVI&TIME=2019-01-01%2F2020-07-26&CRS=EPSG%3A3857&WIDTH=1973&HEIGHT=1449&BBOX=-674196.3859716015%2C4722153.307212234%2C-673018.1808402996%2C4723018.598258993", nombreArchivo)


#Cargamos la imagen:

print(nombreArchivo)
img = cv2.imread(nombreArchivo)
#(Si la imagen está en otro directorio podéis escribir la ruta, p. ej: cv2.imread('/home/minombre/imagenes/bolas_colores.jpg')
 
#Convertimos la imagen a hsv:
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#Nota 1: la constante COLOR_BGR2HSV indica que queremos pasar de BGR a HSV.
#Nota 2: la función cvtColor() también sirve para transformar a otros espacios de color.
 
#Establecemos el rango mínimo y máximo de H-S-V:
# B G R
azul_altos = [np.array([255,255,51]), np.array([256,256,51])]
azul_medios = [np.array([204,204,51]), np.array([205,205,51])]
azul_bajos = [np.array([102,102,0]), np.array([103,103,0])]

amarillo_altos = [np.array([51,255,255]), np.array([51,256,256])]
amarillo_medios = [np.array([51,204,204]), np.array([51,205,205])]
amarillo_bajos = [np.array([0,102, 102]), np.array([0,103,103])]

rojo_altos = [np.array([0,0,254]), np.array([0,0,255])]
rojo_medios = [np.array([0,0,154]), np.array([0,0,155])]
rojo_bajos = [np.array([0,0,102]), np.array([0,0,103])]

verde_altos = [np.array([51,255,52]), np.array([52,255,53])]
verde_medios = [np.array([51,204,51]), np.array([52,204,52])]


"""
amarillo_bajos = np.array([205,205,51])
amarillo_medio = np.array([204,204,51])
amarillo_altos = np.array([255, 255, 51])
"""
#Recordatorio: El rango HSV funciona de la siguiente forma:
#-La 1a componente es la tonalidad (Hue), en nuestro caso amarillo.
#-La 2a componente es la saturación (Saturation) , que hace el color + o - grisáceo.
#-La 3a componente es el valor (Value), que hace el color + o - oscuro.

#Detectamos los píxeles que estén dentro del rango que hemos establecido:
#bajo - alto

def getPixeles(arr_mask):
    if len(arr_mask) == 2:
        return arr_mask[1][1]
    else:
        return 0

"""
MASCARAS AZULES
"""
#TOTAL
mask = cv2.inRange(img, azul_bajos[0], azul_altos[0])
unique, counts = np.unique(mask, return_counts=True)
pixeles_azules = getPixeles(np.asarray((unique, counts)).T)
print('azules', pixeles_azules)
#ALTOS
mask_azul_altos = cv2.inRange(img, azul_altos[0], azul_altos[1])
unique, counts = np.unique(mask_azul_altos, return_counts=True)
pixeles_azules_altos = getPixeles(np.asarray((unique, counts)).T)
print('azules_altos', pixeles_azules_altos)
#MEDIOS
mask_azul_medios = cv2.inRange(img, azul_medios[0], azul_medios[1])
unique, counts = np.unique(mask_azul_medios, return_counts=True)
pixeles_azules_medios = getPixeles(np.asarray((unique, counts)).T)
print('azules_medios', pixeles_azules_medios)
#BAJOS
mask_azul_bajos = cv2.inRange(img, azul_bajos[0], azul_bajos[1])
unique, counts = np.unique(mask_azul_bajos, return_counts=True)
pixeles_azules_bajos = getPixeles(np.asarray((unique, counts)).T)
print('azules_bajos', pixeles_azules_bajos)


"""
MASCARA AMARILLOS
"""
#TOTAL
mask_amarillo = cv2.inRange(img, amarillo_bajos[0], amarillo_altos[0])
unique, counts = np.unique(mask_amarillo, return_counts=True)
pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
print('amarillos', pixeles_amarillos)
#alto
mask_amarillo_altos = cv2.inRange(img, amarillo_altos[0], amarillo_altos[1])
unique, counts = np.unique(mask_amarillo_altos, return_counts=True)
pixeles_amarillos_altos = getPixeles(np.asarray((unique, counts)).T)
print('amarillos_altos', pixeles_amarillos_altos)
#MEDIOS
mask_amarillo_medios = cv2.inRange(img, amarillo_medios[0], amarillo_medios[1])
unique, counts = np.unique(mask_amarillo_medios, return_counts=True)
pixeles_amarillos_medios = getPixeles(np.asarray((unique, counts)).T)
print('amarillos_medios', pixeles_amarillos_medios)
#BAJOS
mask_amarillo_bajos = cv2.inRange(img, amarillo_bajos[0], amarillo_bajos[1])
unique, counts = np.unique(mask_amarillo_bajos, return_counts=True)
pixeles_amarillos_bajos = getPixeles(np.asarray((unique, counts)).T)
print('amarillos_bajos', pixeles_amarillos_bajos)

"""
MASCARA rojo
"""
#TOTAL
mask_rojo = cv2.inRange(img, rojo_bajos[0], rojo_altos[0])
unique, counts = np.unique(mask_rojo, return_counts=True)
pixeles_rojos = getPixeles(np.asarray((unique, counts)).T)
print('rojos', pixeles_rojos)
#alto
mask_rojo_altos = cv2.inRange(img, rojo_altos[0], rojo_altos[1])
unique, counts = np.unique(mask_rojo_altos, return_counts=True)
pixeles_rojos_altos = getPixeles(np.asarray((unique, counts)).T)
print('rojos_altos', pixeles_rojos)
#MEDIOS
mask_rojo_medios = cv2.inRange(img, rojo_medios[0], rojo_medios[1])
unique, counts = np.unique(mask_rojo_medios, return_counts=True)
pixeles_rojos_medios = getPixeles(np.asarray((unique, counts)).T)
print('rojos_medios', pixeles_rojos_medios)
#BAJOS
mask_rojo_bajos = cv2.inRange(img, rojo_bajos[0], rojo_bajos[1])
unique, counts = np.unique(mask_rojo_bajos, return_counts=True)
pixeles_rojos_bajos = getPixeles(np.asarray((unique, counts)).T)
print('rojos_bajos', pixeles_rojos_bajos)

"""
MASCARA VERDES
"""
#TOTAL
mask_verde = cv2.inRange(img, verde_medios[0], verde_altos[0])
unique, counts = np.unique(mask_verde, return_counts=True)
pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
print('rojos', pixeles_verdes)
#ALTO
mask_verde_altos = cv2.inRange(img, verde_altos[0], verde_altos[1])
unique, counts = np.unique(mask_verde_altos, return_counts=True)
pixeles_verdes_altos = getPixeles(np.asarray((unique, counts)).T)
print('rojos_altos', pixeles_verdes_altos)
#MEDIOS
mask_verde_medios = cv2.inRange(img, verde_medios[0], verde_medios[1])
unique, counts = np.unique(mask_verde_medios, return_counts=True)
pixeles_verdes_medios = getPixeles(np.asarray((unique, counts)).T)
print('rojos_medios', pixeles_verdes_medios)




mask_union = cv2.bitwise_or(mask, mask_amarillo)
mask_union2 = cv2.bitwise_or(mask_union, mask_rojo)
mask_union3 = cv2.bitwise_or(mask_union2, mask_verde)


unique, counts = np.unique(mask_union2, return_counts=True)
arr_total = np.asarray((unique, counts)).T
total_pixeles = arr_total[1][1]
print('totalpix', total_pixeles)
suma_capas = sum([pixeles_azules, pixeles_amarillos, pixeles_rojos, pixeles_verdes])

def percentage(part, whole):
    return str(round(100 * float(part)/float(whole), 2))

print('"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')


if total_pixeles == suma_capas:
    print('correcto')
    print('porcentaje de azul ', percentage(pixeles_azules, total_pixeles),'%')
    print('porcentaje de amarillo ', percentage(pixeles_amarillos, total_pixeles),'%')
    print('porcentaje de rojo ', percentage(pixeles_rojos, total_pixeles),'%')
    print('porcentaje de verde ', percentage(pixeles_verdes, total_pixeles),'%')
else:
    print('suma incorrecta')

print('"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')
suma_capas_azules = sum([pixeles_azules_altos, pixeles_azules_bajos, pixeles_azules_medios])
if pixeles_azules == suma_capas_azules:
    print('porcentaje Azul altos', percentage(pixeles_azules_altos, pixeles_azules),'%')
    print('porcentaje Azul medios', percentage(pixeles_azules_medios, pixeles_azules),'%')
    print('porcentaje Azul bajos', percentage(pixeles_azules_bajos, pixeles_azules),'%')

suma_capas_azules = sum([pixeles_azules_altos, pixeles_azules_bajos, pixeles_azules_medios])
if pixeles_azules == suma_capas_azules:
    print('porcentaje Azul altos', percentage(pixeles_azules_altos, pixeles_azules),'%')
    print('porcentaje Azul medios', percentage(pixeles_azules_medios, pixeles_azules),'%')
    print('porcentaje Azul bajos', percentage(pixeles_azules_bajos, pixeles_azules),'%')

print('"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')
print('Total de pixeles de la imagen', total_pixeles)
total_pixeles_azul = {'total': pixeles_azules, 'altos': pixeles_azules_altos, 'medios': pixeles_azules_medios, 'bajos': pixeles_azules_bajos}
total_pixeles_amarillo = {'total': pixeles_amarillos, 'altos': pixeles_amarillos_altos, 'medios': pixeles_amarillos_medios, 'bajos': pixeles_amarillos_bajos}
total_pixeles_rojo = {'total': pixeles_rojos, 'altos': pixeles_rojos_altos, 'medios': pixeles_rojos_medios, 'bajos': pixeles_rojos_bajos}
total_pixeles_verde = {'total': pixeles_verdes, 'altos': pixeles_verdes_altos, 'medios': pixeles_verdes_medios}
print('Pixeles azules', total_pixeles_azul)
print('Pixeles amarillo', total_pixeles_amarillo)
print('Pixeles rojo', total_pixeles_rojo)
print('Pixeles verde', total_pixeles_verde)


#Mostramos la imagen original y la máscara:
#cv2.imshow("Original", img)
#cv2.imshow("Mezcla de todos", mask_union2)

os.rename(nombreArchivo, "imagenes_generadas/"+nombreArchivo)

#Salimos pulsando cualquier tecla:
#print("\nPulsa cualquier tecla para cerrar las ventanas\n")
#cv2.waitKey(0)
#cv2.destroyAllWindows() 