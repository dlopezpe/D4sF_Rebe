import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import uuid
import urllib.request

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

from matplotlib.colors import hsv_to_rgb

img = cv2.imread('ScanParcelas/336975635362682095686805835910542256481.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

def getPixeles(arr_mask):
    if len(arr_mask) == 2:
        return arr_mask[1][1]
    else:
        return 0

def percentage(part, whole):
    return str(round(100 * float(part)/float(whole), 2))


ligth_green = (101, 255, 255)
dark_green = (150, 255, 255)


lo_square = np.full((10, 10, 3), ligth_green, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_green, dtype=np.uint8) / 255.0
plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(lo_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(do_square))
plt.show()

plt.subplot(1, 7, 1)
plt.imshow(img)
#Rojo Naranjas
ligth_green = (1, 255, 0)
dark_green = (25, 255, 255)
mask = cv2.inRange(img_hsv, ligth_green, dark_green)
result = cv2.bitwise_and(img, img, mask=mask)
plt.subplot(1, 7, 2)
plt.imshow(result)
unique, counts = np.unique(mask, return_counts=True)
pixeles_naranjas = getPixeles(np.asarray((unique, counts)).T)
print('Naranjas', pixeles_naranjas)

#AMARILLOS
ligth_green = (26, 255, 0)
dark_green = (50, 255, 255)
mask = cv2.inRange(img_hsv, ligth_green, dark_green)
result = cv2.bitwise_and(img, img, mask=mask)
plt.subplot(1, 7, 3)
plt.imshow(result)
unique, counts = np.unique(mask, return_counts=True)
pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
print('Amarillos', pixeles_amarillos)

#VERDES
ligth_green = (31, 0, 0)
dark_green = (50, 255, 255)
mask = cv2.inRange(img_hsv, ligth_green, dark_green)
result = cv2.bitwise_and(img, img, mask=mask)
plt.subplot(1, 7, 4)
plt.imshow(result)
unique, counts = np.unique(mask, return_counts=True)
pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
print('Verdes', pixeles_verdes)

#AZULES CLARITOS
ligth_green = (51, 255, 0)
dark_green = (100, 255, 255)
mask = cv2.inRange(img_hsv, ligth_green, dark_green)
result = cv2.bitwise_and(img, img, mask=mask)
plt.subplot(1, 7, 5)
plt.imshow(result)
unique, counts = np.unique(mask, return_counts=True)
pixeles_a_claro = getPixeles(np.asarray((unique, counts)).T)
print('Azules Claros', pixeles_a_claro)

#AZULES MEDIO
ligth_green = (101, 255, 0)
dark_green = (115, 255, 255)

mask = cv2.inRange(img_hsv, ligth_green, dark_green)
result = cv2.bitwise_and(img, img, mask=mask)
plt.subplot(1, 7, 6)
plt.imshow(result)
unique, counts = np.unique(mask, return_counts=True)
pixeles_a_medio = getPixeles(np.asarray((unique, counts)).T)
print('Azules Medios', pixeles_a_medio)

#AZULES OSCURO
ligth_green = (116, 255, 0)
dark_green = (200, 255, 255)

mask = cv2.inRange(img_hsv, ligth_green, dark_green)
result = cv2.bitwise_and(img, img, mask=mask)
plt.subplot(1, 7, 7)
plt.imshow(result)
unique, counts = np.unique(mask, return_counts=True)
pixeles_a_oscuro = getPixeles(np.asarray((unique, counts)).T)
print('Azules Medios', pixeles_a_oscuro)



totalPixDetectados = sum([pixeles_naranjas, pixeles_amarillos, pixeles_verdes, pixeles_a_claro, pixeles_a_medio, pixeles_a_oscuro])

print('Total de Pixeles detectados -> ', totalPixDetectados)
print('\n')
print('Porcentaje de Rojo/Naranja -> ', percentage(pixeles_naranjas, totalPixDetectados))
print('Porcentaje de Amarillo ->', percentage(pixeles_amarillos, totalPixDetectados))
print('Porcentaje de Verde ->', percentage(pixeles_verdes, totalPixDetectados))
print('Porcentaje de Azul claro->', percentage(pixeles_a_claro, totalPixDetectados))
print('Porcentaje de Azul Medio ->', percentage(pixeles_a_medio, totalPixDetectados))
print('Porcentaje de Azul Oscuro ->', percentage(pixeles_a_oscuro, totalPixDetectados))

plt.show()

"""
#NARANJAS

light_orange = (1, 190, 200)#Rojo
dark_orange = (25, 255, 255)#Naranja

lo_square = np.full((10, 10, 3), light_orange, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_orange, dtype=np.uint8) / 255.0
plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(do_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(lo_square))
plt.show()

mask = cv2.inRange(img_hsv, light_orange, dark_orange)
result = cv2.bitwise_and(img, img, mask=mask)

plt.subplot(1, 2, 1)
#plt.imshow(mask, cmap="gray")
plt.imshow(img)
plt.subplot(1, 2, 2)
plt.imshow(result)

#cax = plt.axes([0.85, 0.1, 0.075, 0.8])
#plt.colorbar(cax=cax)
plt.colorbar()
plt.show()

"""

#AMARILLOS
"""
ligth_yellow = (26, 255, 255)#Naranja
dark_yellow = (50, 255, 255) #NarajaVerde


lo_square = np.full((10, 10, 3), ligth_yellow, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_yellow, dtype=np.uint8) / 255.0
plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(do_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(lo_square))
plt.show()

mask = cv2.inRange(img_hsv, ligth_yellow, dark_yellow)
result = cv2.bitwise_and(img, img, mask=mask)

plt.subplot(1, 2, 1)
#plt.imshow(mask, cmap="gray")
plt.imshow(img)
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()

#Azules CLaros
ligth_green = (51, 255, 255)
dark_green = (100, 255, 255)

#Azules Oscuros
ligth_green = (101, 255, 255)
dark_green = (255, 255, 255)

------------------------------------------
#NARANJAS / ROJOS
ligth_green = (1, 255, 255)
dark_green = (25, 255, 255)
#AMARILLOS
ligth_green = (26, 255, 255)
dark_green = (50, 255, 255)
#AZULES CLAROS
ligth_green = (51, 255, 255)
dark_green = (100, 255, 255)
#AZULES OSCUROS
ligth_green = (101, 255, 255)
dark_green = (200, 255, 255)
"""

"""
lo_square = np.full((10, 10, 3), ligth_green, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_green, dtype=np.uint8) / 255.0
plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(do_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(lo_square))
plt.show()
"""



"""
#nombreArchivo = str(uuid.uuid1().int)+'.png'
#urllib.request.urlretrieve("https://services.sentinel-hub.com/ogc/wms/13e7a2a7-2e3e-489e-8a65-eb971dab81af?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=false&LAYERS=MOISTURE_INDEX&TIME=2019-01-01%2F2020-07-26&CRS=EPSG%3A3857&WIDTH=1973&HEIGHT=1449&BBOX=-674196.3859716015%2C4722153.307212234%2C-673018.1808402996%2C4723018.598258993", nombreArchivo)


#Cargamos la imagen:

#print(nombreArchivo)
img = cv2.imread('103814560361553475398062767104631236961.png')
#(Si la imagen está en otro directorio podéis escribir la ruta, p. ej: cv2.imread('/home/minombre/imagenes/bolas_colores.jpg')
 
#Convertimos la imagen a hsv:
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#Nota 1: la constante COLOR_BGR2HSV indica que queremos pasar de BGR a HSV.
#Nota 2: la función cvtColor() también sirve para transformar a otros espacios de color.
 
#Establecemos el rango mínimo y máximo de H-S-V:
# B G R
rojo = [np.array([0,0,128]), np.array([1,60,250])]
naranja = [np.array([1, 61, 250]), np.array([1,190,250])]
amarillo = [np.array([1, 191, 250]), np.array([231,255,0])]
verde = [np.array([0,255,232]), np.array([90,255,0])]
azul_claro = [np.array([90,255,0]), np.array([255, 165, 0])]
azul_oscuro = [np.array([249,202,144]), np.array([161,71,13])]



def getPixeles(arr_mask):
    if len(arr_mask) == 2:
        return arr_mask[1][1]
    else:
        return 0

#ROJOS
mask_rojo = cv2.inRange(img, rojo[0], rojo[1])
unique, counts = np.unique(mask_rojo, return_counts=True)
pixeles_rojos = getPixeles(np.asarray((unique, counts)).T)
print('rojos', pixeles_rojos)
#NARANJAS
mask_naranjas = cv2.inRange(img, naranja[0], naranja[1])
unique, counts = np.unique(mask_naranjas, return_counts=True)
pixeles_narajas = getPixeles(np.asarray((unique, counts)).T)
print('naranjas', pixeles_narajas)
#AMARILLOS
mask_amarillos = cv2.inRange(img, amarillo[0], amarillo[1])
unique, counts = np.unique(mask_amarillos, return_counts=True)
pixeles_amarillos = getPixeles(np.asarray((unique, counts)).T)
print('amarillos', pixeles_amarillos)
#VERDE
mask_verdes = cv2.inRange(img, verde[0], verde[1])
unique, counts = np.unique(mask_verdes, return_counts=True)
pixeles_verdes = getPixeles(np.asarray((unique, counts)).T)
print('verdes', pixeles_verdes)
#AZUL CLARO
mask_azul_cla = cv2.inRange(img, azul_claro[0], azul_claro[1])
unique, counts = np.unique(mask_azul_cla, return_counts=True)
pixeles_azul_cla = getPixeles(np.asarray((unique, counts)).T)
print('azul_claro', pixeles_azul_cla)
#AZUL OSCURO
mask_azul_osc = cv2.inRange(hsv, azul_oscuro[0], azul_oscuro[1])
unique, counts = np.unique(mask_azul_osc, return_counts=True)
pixeles_azul_osc = getPixeles(np.asarray((unique, counts)).T)
print('azul_oscuro', pixeles_azul_osc)

cv2.imshow("Original", hsv)
cv2.imshow("Mezcla de todos", mask_azul_osc)


#os.rename(nombreArchivo, "imagenes_generadas/"+nombreArchivo)

print("\nPulsa cualquier tecla para cerrar las ventanas\n")
cv2.waitKey(0)
cv2.destroyAllWindows() 

"""

