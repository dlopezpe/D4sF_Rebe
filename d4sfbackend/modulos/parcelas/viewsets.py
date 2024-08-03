from rest_framework import viewsets, generics, status

from django.core.serializers import serialize

from utils.D4sfConstants import url_api_instances_const
from .models import Parcel, Enterprise
from .serializer import ParcelSerializer, ParcelSerializerFilter, ParcelSerializerFilterNoSentInstance

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.http import HttpResponse

from django.contrib.gis.geos import GEOSGeometry
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
import decimal

import kml2geojson
import os.path

import requests

from sentinelhub import CRS, BBox

from django.contrib.gis.gdal import DataSource
from django.conf import settings

from django.contrib.gis.gdal import OGRGeometry

import sys
#from zipfile import ZipFile
if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile

import json

from modulos.trazas.utils import savelog
from backend.get_username import get_request


class ImportParcelsFromFileViewset(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel
    serializer_class = ParcelSerializerFilterNoSentInstance

    def post(self, request, *args, **kwargs):
        archivo = request.FILES["file"]
        queryset_empresa = Enterprise.objects.filter(id=request.data["enterprise_id"]).first()
        if queryset_empresa:
            enterprise_id = queryset_empresa.id
            enterprise_sentinel_instance = queryset_empresa.sentinel_instance

            # log purpuse
            contextLogs = {
                'user_email': request.user,
                'message': 'Usuario subiendo un .zip from /importparcelsfromfile',
                'status': 'success',
                'extra_data': {
                    'enterprise_id': str(enterprise_id),
                    'enterprise_sentinel_instance': str(enterprise_sentinel_instance),
                    'file': settings.SHAPES_FOLDER+archivo.name
                }
            }
            ##savelog(contextLogs,request)
            # end log purpuse
            
            with open(settings.SHAPES_FOLDER+archivo.name, 'wb') as destination:
                for chunk in archivo.chunks():
                    destination.write(chunk)
                destination.close()
                
                with zipfile.ZipFile(settings.SHAPES_FOLDER+archivo.name, 'r') as zip_ref:
                    zip_ref.extractall(settings.SHAPES_FOLDER)
                    listOfiles = zip_ref.namelist()
                    archivo = ""
                    for elem in listOfiles:
                        if elem.split(".")[1] == 'shp':
                            archivo = elem
                    
                    ds = DataSource(settings.SHAPES_FOLDER+archivo)
                    # check type data firts D4SF-81
                    # D4SF-81: cliente da un nuevo .zip pero el encoing es diferente en el campo FINCA
                    layer = ds[0]
                    if 'OFTInteger' in [ft.__name__ for ft in layer.field_types]:
                        ds = DataSource(settings.SHAPES_FOLDER+archivo,encoding='latin-1') # D4SF-81
                    
                    """
                        1. Sacar todos los poligonos y guardarlos en un Array para compararlos
                        2. Convertir los multipoligonos en poligonos separados para poder compararlos también
                    """
                    arrToCompare = []
                    arrOverlaps = []
                    arrProcesadas = []
                    arrCambiaPoligono = []

                    
                    for layer in ds:
                        for feature in layer:
                            polygon = OGRGeometry(str(feature.geom))
                            areaPolygon = polygon.area
                            
                            available_fields = feature.fields
                            refsigpac = None
                            if 'REFSIGPAC' in available_fields: # D4SF-81
                                refsigpac = str(feature.get("REFSIGPAC"))

                            if str(polygon.geom_name) == 'POLYGON':
                                arrToCompare.append(
                                    {
                                    "FINCA": str(feature.get("FINCA")), 
                                    "ID_FINCA": str(feature.get("ID_FINCA"))+"-0", 
                                    "ID_PRODUCT": str(feature.get("ID_PRODUCT")),
                                    "PRODUCTOR": str(feature.get("PRODUCTOR")), 
                                    "ID_VARIEDA": str(feature.get("ID_VARIEDA")), 
                                    "VARIEDAD": str(feature.get("VARIEDAD")), 
                                    "REFSIGPAC": refsigpac , # str(feature.get("REFSIGPAC"))
                                    "POLYGON": polygon, 
                                    "AREA_CALC" : areaPolygon, 
                                    "AREA_PORC" : 100})
                                
                            elif str(polygon.geom_name) == 'MULTIPOLYGON':
                                index = 0
                                for poligono in list(polygon):
                                    poligonoObj = OGRGeometry(str(poligono))
                                    areaPoligono = poligonoObj.area
                                    porcentajePoligono = (areaPoligono / areaPolygon) * 100
                                    indexPoli = "-"+str(index)

                                    if porcentajePoligono > 99 : 
                                        porcentajePoligono  = 100
                                        indexPoli = "-0"
                                    if porcentajePoligono >= 1 :
                                        arrToCompare.append(
                                            {
                                                "FINCA": str(feature.get("FINCA"))+indexPoli, 
                                                "ID_FINCA": str(feature.get("ID_FINCA"))+indexPoli,  
                                                "ID_PRODUCT": str(feature.get("ID_PRODUCT")), 
                                                "PRODUCTOR": str(feature.get("PRODUCTOR")), 
                                                "ID_VARIEDA": str(feature.get("ID_VARIEDA")), 
                                                "VARIEDAD": str(feature.get("VARIEDAD")), 
                                                "REFSIGPAC": refsigpac , # str(feature.get("REFSIGPAC"))
                                                "POLYGON": poligonoObj,
                                                "AREA_CALC" : areaPoligono,
                                                "AREA_PORC" : porcentajePoligono
                                                    })
                                        index += 1
                    arrCoordinates = []
                    for layer in ds:
                        #print('Layer "%s": %i %ss' % (layer.name, len(layer), layer.geom_type.name))
                        for feature in layer:
                            polygon = OGRGeometry(str(feature.geom))
                            #print("173: ", str(feature.get("ID_FINCA")))
                            areaPolygon = polygon.area
                            if str(polygon.geom_name) == 'POLYGON':
                                overlaps = False 
                                poly = GEOSGeometry(str(feature.geom))
                                if not poly.simple:
                                    arrOverlaps.append("NOT SIMPLE - "+str(feature.get("ID_FINCA"))+" - "+feature.get("FINCA"))
                                    overlaps = True
                                for featurecompare in arrToCompare:
                                    if polygon.overlaps(featurecompare["POLYGON"]):
                                        arrOverlaps.append("OVERLAP - "+str(feature.get("ID_FINCA"))+" - "+feature.get("FINCA")+" CON: "+ str(featurecompare["ID_FINCA"]) +" "+str(featurecompare["FINCA"]))
                                        overlaps = True
                                    if polygon.touches(featurecompare["POLYGON"]):
                                        arrOverlaps.append("TOUCHES - "+str(feature.get("ID_FINCA"))+" - "+feature.get("FINCA")+" CON: "+ str(featurecompare["ID_FINCA"]) +" "+str(featurecompare["FINCA"]))
                                        overlaps = True
                                if not overlaps:
                                    if str(polygon.geom_name) == 'POLYGON':
                                        jsonObj = json.loads(polygon.json)
                                        if len(jsonObj["coordinates"]):
                                            arrCoordinates.append(jsonObj["coordinates"])
                                            arrProcesadas.append(str(feature.get("FINCA"))+" - "+str(feature.get("ID_FINCA")))

                            elif str(polygon.geom_name) == 'MULTIPOLYGON':
                                overlaps = False
                                index = 0
                                for poligono in list(polygon):
                                    poligonoObj = OGRGeometry(str(poligono))
                                    poly = GEOSGeometry(str(poligono))
                                    areaPoligono = poligonoObj.area
                                    porcentajePoligono = (areaPoligono / areaPolygon) * 100
                                    indexPoli = "-"+str(index)
                                    if porcentajePoligono > 99 : 
                                        porcentajePoligono  = 100
                                        indexPoli = ""
                                    if porcentajePoligono >= 1 :
                                        if not poly.simple:
                                            arrOverlaps.append("NOT SIMPLE - "+str(feature.get("ID_FINCA"))+indexPoli+" - "+feature.get("FINCA")+indexPoli)
                                            overlaps = True
                                        for featurecompare in arrToCompare:
                                            if poligonoObj.overlaps(featurecompare["POLYGON"]):
                                                arrOverlaps.append("OVERLAP - "+str(feature.get("ID_FINCA"))+indexPoli+" - "+feature.get("FINCA")+" CON: "+ str(featurecompare["ID_FINCA"])+" "+str(featurecompare["FINCA"]))
                                                overlaps = True
                                            if poligonoObj.touches(featurecompare["POLYGON"]):
                                                arrOverlaps.append("TOUCHES - "+str(feature.get("ID_FINCA"))+indexPoli+" - "+feature.get("FINCA")+" CON: "+ str(featurecompare["ID_FINCA"])+" "+str(featurecompare["FINCA"]))
                                                overlaps = True
                                        if not overlaps:
                                            jsonObj = json.loads(poligonoObj.json)
                                            if len(jsonObj["coordinates"]):
                                                arrCoordinates.append(jsonObj["coordinates"])
                                                arrProcesadas.append(str(feature.get("FINCA")) +indexPoli+" - "+str(feature.get("ID_FINCA"))+indexPoli)
                                        index += 1
                    
                        # miramos si alguna parcela ha cambiado
                        for parcela in arrToCompare:
                            try:
                                #queryset_parcela = Parcel.objects.filter(id_importado=parcela["ID_FINCA"], enterprise=enterprise_id).first()
                                sufijo=parcela["ID_FINCA"].split("-")
                                queryset_parcela = Parcel.objects.filter(id_importado=sufijo[0], id_sufijo=sufijo[1], enterprise=enterprise_id).first()
                                # Si existe, miramos si coinciden las coordenadas con la anterior
                                if queryset_parcela:
                                    # queryset_parcela_coord = Parcel.objects.filter(id_importado=parcela["ID_FINCA"], enterprise=enterprise_id, polygon_init = str(parcela["POLYGON"])).first()
                                    parcela_inicial = str(queryset_parcela.polygon_init).replace("SRID=4326;", "").replace(", ", ",")
                                    if(str(parcela["POLYGON"]) != parcela_inicial) :
                                        
                                        arrCambiaPoligono.append("MODIFICADA -> " + str(parcela.get("FINCA"))+" - "+str(parcela.get("ID_FINCA")))
                                else:
                                    
                                    arrCambiaPoligono.append("NUEVA -> " + str(parcela.get("FINCA"))+" - "+str(parcela.get("ID_FINCA")))
                            except Exception as Error:
                                print(parcela["ID_FINCA"])
                                print(str(Error))






                    # Confirmación de importación
                    if request.data["confirm_import"] == "true":

                        # Borramos todas las parcelas de la empresa
                        # Insertamos todas las parcelas nuevas en la empresa
                        
                        # Borrado de las parcelas que tengan el id_importado a NULL
                        Parcel.objects.filter(enterprise=enterprise_id, id_importado__isnull=True).delete()
                        #parcela["ID_PRODUCT"] = 173
                        for parcela in arrToCompare:
                            try:

                                LYC=False
                                if parcela['VARIEDAD']=="AGRAZ 6" or parcela['VARIEDAD']=="H-1311" or parcela['VARIEDAD']=="KGM 121":
                                    LYC=True
                                    print('-----',parcela['VARIEDAD'],"=",LYC,'-----')
                                sufijo=parcela["ID_FINCA"].split("-")
                                # todo
                                # queryset_parcela = Parcel.objects.filter(id_importado=sufijo[0], id_sufijo=sufijo[1], enterprise=enterprise_id).first()
                                queryset_parcela = Parcel.objects.filter(id_importado=sufijo[0], id_sufijo=sufijo[1], enterprise=enterprise_id, deleted_at__isnull=True).first()

                                #print("parcela",parcela)
                                area_float = round(float(parcela["POLYGON"].area*1000000), 2)
                                if queryset_parcela:
                                    # Si la parcela existe, la actualizamos
                                    parcela_inicial = str(queryset_parcela.polygon_init).replace("SRID=4326;", "").replace(", ", ",")
                                    if(str(parcela["POLYGON"]) == parcela_inicial) :
                                        print("Editado",parcela["ID_FINCA"])
                                        # Si no han cambiado las coordenadas iniciales, no actualizamos el poligono para no estropear los cambios que teniamos
                                        # eliminamos actualizar campo description y nombre ver email: Desarrollo parcelas confirmado - Agraz.
                                        serializer = ParcelSerializer(queryset_parcela, data={"area": area_float, "enterprise": enterprise_id, "user_created": str(request.user.id), "id_importado": sufijo[0], "id_productor_importado": parcela["ID_PRODUCT"], "productor_importado": parcela["PRODUCTOR"], "id_variedad_importado": parcela["ID_VARIEDA"], "variedad_importado": parcela["VARIEDAD"], "sigpac_importado": parcela["REFSIGPAC"], "area_calc" : parcela["AREA_CALC"], "area_porc" : parcela["AREA_PORC"], "id_sufijo":sufijo[1], "is_LYC":LYC})
                                    else:
                                        print("Editado poligono",parcela["ID_FINCA"])
                                        # Si han cambiado las coordenadas iniciales, cambiamos el poligono, tanto el actual como el inicial
                                        # eliminamos actualizar campo description y nombre ver email: Desarrollo parcelas confirmado - Agraz.
                                        serializer = ParcelSerializer(queryset_parcela, data={"area": area_float,  "polygon": str(parcela["POLYGON"]), "enterprise": enterprise_id, "user_created": str(request.user.id), "id_importado": sufijo[0], "id_productor_importado": parcela["ID_PRODUCT"], "productor_importado": parcela["PRODUCTOR"], "id_variedad_importado": parcela["ID_VARIEDA"], "variedad_importado": parcela["VARIEDAD"], "sigpac_importado": parcela["REFSIGPAC"], "polygon_init": str(parcela["POLYGON"]), "area_calc" : parcela["AREA_CALC"], "area_porc" : parcela["AREA_PORC"], "id_sufijo":sufijo[1], "is_LYC":LYC})
                                else:
                                    # Si la parcela es nueva, la insertamos
                                    print ("Nueva parcela",parcela["ID_FINCA"])
                                    serializer = ParcelSerializer(data={"name": parcela["FINCA"], "description": parcela["ID_FINCA"], "area": area_float,  "polygon": str(parcela["POLYGON"]), "enterprise": enterprise_id, "user_created": str(request.user.id), "id_importado": sufijo[0], "id_productor_importado": parcela["ID_PRODUCT"], "productor_importado": parcela["PRODUCTOR"], "id_variedad_importado": parcela["ID_VARIEDA"], "variedad_importado": parcela["VARIEDAD"], "sigpac_importado": parcela["REFSIGPAC"], "polygon_init": str(parcela["POLYGON"]), "area_calc" : parcela["AREA_CALC"], "area_porc" : parcela["AREA_PORC"], "id_sufijo":sufijo[1], "is_LYC":LYC})
                                    
                                serializer.is_valid(raise_exception=True)
                                serializer.save()

                            except Exception as Error:
                                print(str(Error))
                        
                        
                        
                        
                        # log purpuse
                        contextLogs = {
                            'user_email': request.user,
                            'message': 'Parcelas guardadas del .zip from /importparcelsfromfile',
                            'status': 'success',
                            'extra_data': {
                                'enterprise_id': str(enterprise_id),
                                'enterprise_sentinel_instance': str(enterprise_sentinel_instance),
                            }
                        }
                        ##savelog(contextLogs,request)
                        # end log purpuse

                        try:
                            client_id = '33467c23-fada-4405-8a5b-33ee38169273'
                            client_secret = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
                            client = BackendApplicationClient(client_id=client_id)
                            oauth = OAuth2Session(client=client)
                            token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token', client_id=client_id, client_secret=client_secret)
                            hed = {
                                'Content-Type': 'application/json;charset=utf-8',
                                'Authorization': 'Bearer '+token['access_token']
                            }
                            data = {
                                'name': str(enterprise_id),
                                    "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                                'additionalData': {
                                    'showLogo': False,
                                    'showWarnings': False,
                                    'imageQuality': 30,
                                    'disabled': False
                                },
                                'areaOfInterest': {
                                    'type': 'MultiPolygon',
                                    'coordinates': arrCoordinates
                                    ,'crs': {
                                        'type':'name',
                                        'properties': {
                                            'name': 'urn:ogc:def:crs:EPSG::4326'
                                        }
                                    }
                                },
                            }
                            urlS = url_api_instances_const+str(enterprise_sentinel_instance)
                            reponses = requests.request("PUT", urlS, headers=hed, data = json.dumps(data))
                                #print(reponses.text.encode('utf8'))
                        except Exception as Error:
                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'Fallo PUT sentinel request /importparcelsfromfile',
                                'status': 'error',
                                'extra_data': {
                                    'enterprise_id': str(enterprise_id),
                                    'error': str(Error),
                                }
                            }
                            ##savelog(contextLogs,request)
                            # end log purpuse
                        
                        
                               
            return Response({"procesadas": arrProcesadas, "Overlaps": arrOverlaps, "totalparcelas": len(arrToCompare), "cambiadas": arrCambiaPoligono}, status=status.HTTP_200_OK)
        
        # log purpuse
        contextLogs = {
            'user_email': request.user,
            'message': 'No se puede procesar en /importparcelsfromfile',
            'status': 'warning',
            'extra_data': {
            }
        }
        #savelog(contextLogs,request)
        # end log purpuse
        return Response({"procesadas": "No se puede procesar", "Overlaps": "No se puede procesar", "totalparcelas": "No se puede procesar"}, status=status.HTTP_400_BAD_REQUEST)


#IMPORTACION DE UN ARCHIVO DESDE GEOJSON
class ImportParcelsFromGeoJSONViewset(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel
    serializer_class = ParcelSerializerFilterNoSentInstance

    def post(self, request, *args, **kwargs):
        archivo = request.FILES["file"]
        queryset_empresa = Enterprise.objects.filter(id=request.data["enterprise_id"]).first()
        if queryset_empresa:
            enterprise_id = queryset_empresa.id
            enterprise_sentinel_instance = queryset_empresa.sentinel_instance
            # log purpuse
            contextLogs = {
                'user_email': request.user,
                'message': 'Usuario subiendo un .zip (geojson) from /importparcelsfromGeoJSON',
                'status': 'success',
                'extra_data': {
                    'enterprise_id': str(enterprise_id),
                    'enterprise_sentinel_instance': str(enterprise_sentinel_instance),
                    'file': settings.SHAPES_FOLDER+archivo.name,
                    'borrado': request.data['borrado'],
                    'confirm_import': request.data['confirm_import']
                }
            }
            #savelog(contextLogs,request)
            # end log purpuse
            documentPath = settings.SHAPES_FOLDER+archivo.name
            with open(documentPath, 'wb') as destination:
                for chunk in archivo.chunks():
                    destination.write(chunk)
                destination.close()
                with zipfile.ZipFile(settings.SHAPES_FOLDER+archivo.name, 'r') as zip_ref:
                    zip_ref.extractall(settings.SHAPES_FOLDER)
                    listOfiles = zip_ref.namelist()
            
                arrToCompare = []
                arrOverlaps = []
                arrProcesadas = []
                arrCambiaPoligono = []
                for file in listOfiles:
                    dir=settings.SHAPES_FOLDER+file
                    ds = DataSource(dir)
                    for layer in ds:
                        indexPoli=0
                        for feature in layer:
                            corte=str(file).split('/')
                            nombre=corte[0][0:]
                            nombre=nombre[:-8]
                            polygon = OGRGeometry(str(feature.geom))
                            areaPolygon = polygon.area
                            nombreParcela=nombre+"-"+str(indexPoli)
                            if str(polygon.geom_name) == 'POLYGON':
                                arrToCompare.append({"FINCA": nombreParcela, "POLYGON": polygon, "AREA_CALC" : areaPolygon, "AREA_PORC" : 100})
                            indexPoli+=1
                arrCoordinates = []
                

                for file in listOfiles:
                    dir=settings.SHAPES_FOLDER+file
                    ds = DataSource(dir)
                    for layer in ds:
                        indexPoli=0
                        for feature in layer:
                            corte=str(file).split('/')
                            nombre=corte[0][0:]
                            nombre=nombre[:-8]
                            polygon = OGRGeometry(str(feature.geom))
                            nombreParcela=nombre+"-"+str(indexPoli)
                            areaPolygon = polygon.area
                            if str(polygon.geom_name) == 'POLYGON':
                                overlaps = False 
                                poly = GEOSGeometry(str(feature.geom))
                                if not poly.simple:
                                    arrOverlaps.append("NOT SIMPLE - "+nombreParcela)
                                    overlaps = True
                                for featurecompare in arrToCompare:
                                    if polygon.overlaps(featurecompare["POLYGON"]):
                                        arrOverlaps.append("OVERLAP - "+nombreParcela+" CON: "+str(featurecompare["FINCA"]))
                                        overlaps = True
                                    if polygon.touches(featurecompare["POLYGON"]):
                                        arrOverlaps.append("TOUCHES - "+nombreParcela+" CON: "+str(featurecompare["FINCA"]))
                                        overlaps = True
                                if not overlaps:
                                    if str(polygon.geom_name) == 'POLYGON':
                                        jsonObj = json.loads(polygon.json)
                                        if len(jsonObj["coordinates"]):
                                            arrCoordinates.append(jsonObj["coordinates"])
                                            arrProcesadas.append(nombreParcela)
                            indexPoli+=1
                
                # Confirmación de importación
                if request.data["confirm_import"] == "true":

                    if request.data["borrado"] == "true":
                        # Borramos todas las parcelas de la empresa
                        Parcel.objects.filter(enterprise=enterprise_id).delete()
                    # Insertamos todas las parcelas nuevas en la empresa
                    # Borrado de las parcelas que tengan el id_importado a NULL
                    #Parcel.objects.filter(enterprise=enterprise_id, id_importado__isnull=True).delete()

                    # Recorremos las parcelas del fichero y actualizamos los datos en la bddd
                    for parcela in arrToCompare:
                        try:
                            LYC=False
                            area_float = round(float(parcela["POLYGON"].area*1000000), 2)
                            serializer = ParcelSerializer(data={"name": parcela["FINCA"], "area": area_float,  "polygon": str(parcela["POLYGON"]), "enterprise": enterprise_id, "user_created": str(request.user.id), "polygon_init": str(parcela["POLYGON"]), "area_calc" : parcela["AREA_CALC"], "area_porc" : parcela["AREA_PORC"], "is_LYC":LYC})
                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                        except Exception as Error:
                            print(str(Error))
                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'error guardar parcelas del .zip (geojson) /importparcelsfromGeoJSON',
                                'status': 'error',
                                'extra_data': {
                                    'enterprise_id': str(enterprise_id),
                                    'enterprise_sentinel_instance': str(enterprise_sentinel_instance),
                                    'file': documentPath,
                                    'error':str(Error),
                                }
                            }
                            #savelog(contextLogs,request)
                    
                    
                    try:
                        client_id = '33467c23-fada-4405-8a5b-33ee38169273'
                        client_secret = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
                        client = BackendApplicationClient(client_id=client_id)
                        oauth = OAuth2Session(client=client)
                        token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token', client_id=client_id, client_secret=client_secret)
                        hed = {
                            'Content-Type': 'application/json;charset=utf-8',
                            'Authorization': 'Bearer '+token['access_token']
                        }
                        data = {
                            'name': str(enterprise_id),
                            "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                            'additionalData': {
                                'showLogo': False,
                                'showWarnings': False,
                                'imageQuality': 30,
                                'disabled': False
                            },
                            'areaOfInterest': {
                                'type': 'MultiPolygon',
                                'coordinates': arrCoordinates
                                ,'crs': {
                                    'type':'name',
                                    'properties': {
                                        'name': 'urn:ogc:def:crs:EPSG::4326'
                                    }
                                }
                            },
                        }
                        urlS = url_api_instances_const+str(enterprise_sentinel_instance)
                        reponses = requests.request("PUT", urlS, headers=hed, data = json.dumps(data))
                    except Exception as Error:
                        # log purpuse
                        contextLogs = {
                            'user_email': request.user,
                            'message': 'Fallo PUT sentinel request /importparcelsfromGeoJSON',
                            'status': 'error',
                            'extra_data': {
                                'enterprise_id': str(enterprise_id),
                                'error': str(Error),
                                'file': documentPath
                            }
                        }
                        #savelog(contextLogs,request)
                        # end log purpuse
                        
            return Response({"procesadas": arrProcesadas, "Overlaps": arrOverlaps, "totalparcelas": len(arrToCompare), "cambiadas": arrCambiaPoligono}, status=status.HTTP_200_OK)
        return Response({"procesadas": "No se puede procesar", "Overlaps": "No se puede procesar", "totalparcelas": "No se puede procesar"}, status=status.HTTP_400_BAD_REQUEST)


class ImportParcelsFromFileKMLViewset(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel
    serializer_class = ParcelSerializerFilterNoSentInstance

    def post(self, request, *args, **kwargs):
        data=[]
        archivo = request.FILES["file"]
        client = request.POST.get("client", False) # flag for new client import document
        
        
        extension = os.path.splitext(archivo.name)[1]
        queryset_empresa = Enterprise.objects.filter(id=request.data["enterprise_id"]).first()
        if queryset_empresa:
            enterprise_id = queryset_empresa.id
            enterprise_sentinel_instance = queryset_empresa.sentinel_instance

            # log purpuse
            contextLogs = {
                'user_email': request.user,
                'message': 'Usuario subiendo un .zip from /parcelasImportFromFileKML',
                'status': 'success',
                'extra_data': {
                    'enterprise_id': str(enterprise_id),
                    'enterprise_sentinel_instance': str(enterprise_sentinel_instance),
                    'file': settings.SHAPES_FOLDER+archivo.name,
                    'extension': extension
                }
            }
            ##savelog(contextLogs,request)
            # end log purpuse
           
            arrToCompare = []
            arrOverlaps = []
            arrProcesadas = []
            arrCambiaPoligono = []

            documentPath = settings.SHAPES_FOLDER+archivo.name
            with open(documentPath, 'wb') as destination:
                
                for chunk in archivo.chunks():
                    destination.write(chunk)
                destination.close()
                
                try:
                #EN CASO DE QUE ENTRE UN ARCHIVO KML
                    if extension=='.kml':
                        kml2geojson.main.convert(settings.SHAPES_FOLDER+archivo.name, archivo.name)
                        ds = DataSource(settings.SHAPES_FOLDER+archivo.name)
                        arrToCompare = []
                        arrOverlaps = []
                        arrProcesadas = []
                        arrCambiaPoligono = []

                        for layer in ds:
                            for feature in layer:
                                polygon = OGRGeometry(str(feature.geom))
                                areaPolygon = polygon.area
                                    # D4SF-83
                                parcelaName = feature.get("Parcela") if "Parcela" in feature.fields else feature.get("Name")
                                parcelaProductor = feature.get("Produtor") if "Produtor" in feature.fields else 'default'
                                parcelaVariedade = feature.get("Variedade") if "Variedade" in feature.fields else 'default'

                                    
                                if str(polygon.geom_name) == 'POLYGON':
                                        arrToCompare.append({"FINCA": str(parcelaName), "PRODUCTOR": str(parcelaProductor), "VARIEDAD": str(parcelaVariedade), "POLYGON": polygon, "AREA_CALC" : areaPolygon, "AREA_PORC" : 100})
                                elif str(polygon.geom_name) == 'MULTIPOLYGON':
                                    index = 0
                                    for poligono in list(polygon):
                                        poligonoObj = OGRGeometry(str(poligono))
                                        areaPoligono = poligonoObj.area
                                            
                                        porcentajePoligono = (areaPoligono / areaPolygon) * 100
                                        indexPoli = "-"+str(index)

                                        if porcentajePoligono > 99 : 
                                            porcentajePoligono  = 100
                                            indexPoli = "-0"
                                        if porcentajePoligono >= 1 :
                                                arrToCompare.append(
                                                    {
                                                        "FINCA": str(parcelaName) +indexPoli,
                                                        "PRODUCTOR": str(parcelaProductor), 
                                                        "VARIEDAD": str(parcelaVariedade), 
                                                        "POLYGON": poligonoObj, 
                                                        "AREA_CALC" : areaPoligono, 
                                                        "AREA_PORC" : porcentajePoligono
                                                    }
                                                )
                                                index += 1
                        arrCoordinates = []

                        for layer in ds:
                            for feature in layer:
                                polygon = OGRGeometry(str(feature.geom))
                                areaPolygon = polygon.area
                                    
                                    # D4SF-83
                                parcelaFinca = feature.get("FINCA") if "FINCA" in feature.fields else 'default'
                                parcelaName = feature.get("Parcela") if "Parcela" in feature.fields else feature.get("Name")
                                parcelaProductor = feature.get("Produtor") if "Produtor" in feature.fields else 'default'
                                parcelaVariedade = feature.get("Variedade") if "Variedade" in feature.fields else 'default'

                                print("parcelaName: "+str(parcelaName))

                                if str(polygon.geom_name) == 'POLYGON':
                                    overlaps = False 
                                    poly = GEOSGeometry(str(feature.geom))
                                    if not poly.simple:
                                        arrOverlaps.append("NOT SIMPLE - "+ parcelaFinca) # feature.get("FINCA")
                                        overlaps = True
                                    for featurecompare in arrToCompare:
                                        if polygon.overlaps(featurecompare["POLYGON"]):
                                            arrOverlaps.append("OVERLAP - "+str(parcelaFinca)+" CON: "+str(featurecompare["FINCA"]))
                                            overlaps = True
                                        if polygon.touches(featurecompare["POLYGON"]):
                                            arrOverlaps.append("TOUCHES - "+str(parcelaName)+" CON: "+str(featurecompare["FINCA"]))
                                            overlaps = True
                                    if not overlaps:
                                        if str(polygon.geom_name) == 'POLYGON':
                                            jsonObj = json.loads(polygon.json)
                                            if len(jsonObj["coordinates"]):
                                                arrCoordinates.append(jsonObj["coordinates"])
                                                arrProcesadas.append(str(parcelaName))
                        
                                elif str(polygon.geom_name) == 'MULTIPOLYGON':
                                    overlaps = False
                                    index = 0
                                    for poligono in list(polygon):
                                            
                                        poligonoObj = OGRGeometry(str(poligono))
                                        poly = GEOSGeometry(str(poligono))
                                            
                                        areaPoligono = poligonoObj.area
                                        porcentajePoligono = (areaPoligono / areaPolygon) * 100
                                        indexPoli = "-"+str(index)
                                        if porcentajePoligono > 99 : 
                                            porcentajePoligono  = 100
                                            indexPoli = ""
                                        if porcentajePoligono >= 1 :
                                            if not poly.simple:
                                                arrOverlaps.append("NOT SIMPLE - "+str(parcelaName)+indexPoli)
                                                overlaps = True
                                            for featurecompare in arrToCompare:
                                                if poligonoObj.overlaps(featurecompare["POLYGON"]):
                                                    arrOverlaps.append("OVERLAP - "+str(parcelaName)+indexPoli+" CON: "+str(featurecompare["FINCA"]))
                                                    overlaps = True
                                                if poligonoObj.touches(featurecompare["POLYGON"]):
                                                    arrOverlaps.append("TOUCHES - "+str(parcelaName)+indexPoli+" CON: "+str(featurecompare["FINCA"]))
                                                    overlaps = True
                                            if not overlaps:
                                                jsonObj = json.loads(poligonoObj.json)
                                                if len(jsonObj["coordinates"]):
                                                    arrCoordinates.append(jsonObj["coordinates"])
                                                    arrProcesadas.append(str(parcelaName))
                                            index += 1


                    #EN CASO DE QUE ENTRE UN ARCHIVO KMZ
                        if extension=='.kmz' and client is False:
                            with zipfile.ZipFile(settings.SHAPES_FOLDER+archivo.name, 'r') as zip_ref:
                                zip_ref.extractall(settings.SHAPES_FOLDER)
                                listOfiles = zip_ref.namelist()
                                archivo = ""
                                    
                                for elem in listOfiles:
                                    if elem.split(".")[1] == 'kml':
                                        archivo = elem
                                kml2geojson.main.convert(settings.SHAPES_FOLDER+archivo, archivo)
                                ds = DataSource(settings.SHAPES_FOLDER+archivo)
                            
                        nombre=""
                        productor=""
                        variedad=""

                        for layer in ds:
                            for feature in layer:
                                corte=str(feature.get('description')).split('td')
                                nombre=corte[18][1:]
                                nombre=nombre[:-2]
                                productor=corte[26][1:]
                                productor=productor[:-2]
                                variedad=corte[51][1:]
                                variedad=variedad[:-2]
                                polygon = OGRGeometry(str(feature.geom))
                                if polygon.geom_type == 'MultiPolygon25D':
                                    indexPoli=0
                                    for poly in polygon:
                                        poly.coord_dim = 2
                                        nombreParcela=nombre+"-"+str(indexPoli)
                                        areaPolygon = poly.area
                                        if str(poly.geom_name) == 'POLYGON':
                                            arrToCompare.append({"FINCA": nombreParcela+" - "+productor, "PRODUCTOR": productor, "VARIEDAD": variedad, "POLYGON": poly, "AREA_CALC" : areaPolygon, "AREA_PORC" : 100})
                                        indexPoli+=1    
                        arrCoordinates = []

                        for layer in ds:
                            for feature in layer:
                                corte=str(feature.get('description')).split('td')
                                nombre=corte[18][1:]
                                nombre=nombre[:-2]
                                productor=corte[26][1:]
                                productor=productor[:-2]
                                variedad=corte[51][1:]
                                variedad=variedad[:-2]


                                polygon = OGRGeometry(str(feature.geom))
                                if polygon.geom_type == 'MultiPolygon25D':
                                    indexPoli=0
                                    for item in polygon:
                                        item.coord_dim = 2
                                        nombreParcela=nombre+"-"+str(indexPoli)
                                        areaPolygon = item.area
                                        if str(item.geom_name) == 'POLYGON':
                                            overlaps = False 
                                            poly = GEOSGeometry(str(feature.geom))
                                            if not poly.simple:
                                                arrOverlaps.append("NOT SIMPLE - "+nombreParcela+" - "+productor)
                                                overlaps = True
                                            for featurecompare in arrToCompare:
                                                if item.overlaps(featurecompare["POLYGON"]):
                                                    arrOverlaps.append("OVERLAP - "+nombreParcela+" - "+productor+" CON: "+str(featurecompare["FINCA"]))
                                                    overlaps = True
                                                if item.touches(featurecompare["POLYGON"]):
                                                    arrOverlaps.append("TOUCHES - "+nombre+" - "+productor+" CON: "+str(featurecompare["FINCA"]))
                                                    overlaps = True
                                            if not overlaps:
                                                if str(item.geom_name) == 'POLYGON':
                                                    jsonObj = json.loads(polygon.json)
                                                    if len(jsonObj["coordinates"]):
                                                        arrCoordinates.append(jsonObj["coordinates"])
                                                        arrProcesadas.append(nombreParcela+" - "+productor)
                                                            
                                            indexPoli+=1
                                                
                        # new file for Multitomate client 
                        if extension=='.kmz' and client:
                            with zipfile.ZipFile(settings.SHAPES_FOLDER+archivo.name, 'r') as zip_ref:
                                zip_ref.extractall(settings.SHAPES_FOLDER)
                                listOfiles = zip_ref.namelist()
                                archivo = ""
                                
                                # get fil .kml on the list files
                                for elem in listOfiles:
                                    if elem.split(".")[1] == 'kml':
                                        archivo = elem
                                
                                kml2geojson.main.convert(settings.SHAPES_FOLDER+archivo, archivo)
                                ds = DataSource(settings.SHAPES_FOLDER+archivo)

                            nombre=""
                            productor=""
                            variedad=""

                            for layer in ds:
                                for feature in layer:
                                    corte = str(feature.get('name')).split('Placemark')
                                    polygon = OGRGeometry(str(feature.geom))
                                    indexPoli=0
                                    
                                    newPolygon = polygon
                                    newPolygon.coord_dim = 2
                                    nombreParcela = corte[0] + "-" + str(indexPoli)
                                    areaPolygon = newPolygon.area
                                    if str(newPolygon.geom_name) == 'POLYGON':
                                            arrToCompare.append({"FINCA": nombreParcela+" - "+productor, "PRODUCTOR": productor, "VARIEDAD": variedad, "POLYGON": newPolygon, "AREA_CALC" : areaPolygon, "AREA_PORC" : 100})
                                            indexPoli+=1 




                            arrCoordinates = [] 

                            for layer in ds:
                                for feature in layer:
                                    corte = str(feature.get('name')).split('Placemark')
                                    
                                    nombre = corte[0]
                                    productor = corte[0]
                                    variedad = corte[0]
                                    


                                    polygon = OGRGeometry(str(feature.geom))
                                    indexPoli = 0

                                    
                                    newPolygon = polygon
                                    
                                    newPolygon.coord_dim = 2
                                    nombreParcela=nombre+"-"+str(indexPoli)
                                    areaPolygon = newPolygon.area
                                    if str(newPolygon.geom_name) == 'POLYGON':
                                        overlaps = False 
                                        poly = GEOSGeometry(str(feature.geom))
                                        if not poly.simple:
                                            arrOverlaps.append("NOT SIMPLE - "+nombreParcela+" - "+productor)
                                            overlaps = True
                                        for featurecompare in arrToCompare:
                                            if newPolygon.overlaps(featurecompare["POLYGON"]):
                                                arrOverlaps.append("OVERLAP - "+nombreParcela+" - "+productor+" CON: "+str(featurecompare["FINCA"]))
                                                overlaps = True
                                            if newPolygon.touches(featurecompare["POLYGON"]):
                                                arrOverlaps.append("TOUCHES - "+nombre+" - "+productor+" CON: "+str(featurecompare["FINCA"]))
                                                overlaps = True
                                        if not overlaps:
                                            if str(newPolygon.geom_name) == 'POLYGON':
                                                jsonObj = json.loads(polygon.json)
                                                if len(jsonObj["coordinates"]):
                                                    arrCoordinates.append(jsonObj["coordinates"])
                                                    arrProcesadas.append(nombreParcela+" - "+productor)
                                        indexPoli+=1
                except Exception as Error:
                    print(str(Error))
                    # log purpuse
                    # posible falso positivo si se importa archivo D4SF-83
                    contextLogs = {
                        'user_email': request.user,
                        'message': 'error desestructurado los datos del .zip /parcelasImportFromFileKML',
                        'status': 'error',
                        'extra_data': {
                            'enterprise_id': str(enterprise_id),
                            'file': documentPath,
                            'error':str(Error),
                            'extension': extension
                        }
                    }
                    ##savelog(contextLogs,request)
                    # end log purpuse



                    # Confirmación de importación
                    if request.data["confirm_import"] == "true":
                        # Borramos todas las parcelas de la empresa
                        Parcel.objects.filter(enterprise=enterprise_id).delete()
                        # Insertamos todas las parcelas nuevas en la empresa
                        # Borrado de las parcelas que tengan el id_importado a NULL
                        
                        #Parcel.objects.filter(enterprise=enterprise_id, id_importado__isnull=True).delete()

                        # Recorremos las parcelas del fichero y actualizamos los datos en la bddd
                        for parcela in arrToCompare:
                            
                            if extension=='.kmz' and client:
                                # todo change to prod
                                parcela['VARIEDAD'] = 'Import .kmz'
                                parcela['PRODUCTOR'] = 'Hit 22'
                            
                            try:
                                LYC=False
                                if parcela['VARIEDAD']=="AGRAZ 6" or parcela['VARIEDAD']=="H-1311" or parcela['VARIEDAD']=="KGM 121":
                                    LYC=True
                                area_float = round(float(parcela["POLYGON"].area*1000000), 2)
                                
                                
                                # D4SF-83
                                newPolygon = parcela["POLYGON"]
                                newPolygon.coord_dim = 2
                                
                                serializer = ParcelSerializer(
                                    data={
                                        "name": parcela["FINCA"],
                                        "area": area_float,  
                                        "polygon": str(newPolygon), 
                                        "enterprise": enterprise_id, 
                                        "user_created": str(request.user.id), 
                                        "productor_importado": parcela["PRODUCTOR"], 
                                        "variedad_importado": parcela["VARIEDAD"], 
                                        "polygon_init": str(newPolygon), 
                                        "area_calc" : parcela["AREA_CALC"], 
                                        "area_porc" : parcela["AREA_PORC"], 
                                        "is_LYC":LYC
                                    }
                                )
                                serializer.is_valid(raise_exception=True)
                                print("Guardando parcela: ", parcela["FINCA"])
                                serializer.save()

                            except Exception as Error:
                                # log purpuse
                                contextLogs = {
                                    'user_email': request.user,
                                    'message': 'error en la carga del .zip /parcelasImportFromFileKML',
                                    'status': 'error',
                                    'extra_data': {
                                        'enterprise_id': str(enterprise_id),
                                        'file': settings.SHAPES_FOLDER+archivo.name,
                                        'error':str(Error),
                                        'extension': extension
                                    }
                                }
                                ##savelog(contextLogs,request)
                                # end log purpuse
                                print("****Error*****")
                                print(str(Error))
                        
                        try:
                            client_id = '33467c23-fada-4405-8a5b-33ee38169273'
                            client_secret = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
                            client = BackendApplicationClient(client_id=client_id)
                            oauth = OAuth2Session(client=client)
                            token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token', client_id=client_id, client_secret=client_secret)
                            hed = {
                                'Content-Type': 'application/json;charset=utf-8',
                                'Authorization': 'Bearer '+token['access_token']
                            }
                            data = {
                                'name': str(enterprise_id),
                                    "userId": "6b9e0c32-9a47-4c08-bb44-8a5b7c178c41",
                                'additionalData': {
                                    'showLogo': False,
                                    'showWarnings': False,
                                    'imageQuality': 30,
                                    'disabled': False
                                },
                                'areaOfInterest': {
                                    'type': 'MultiPolygon',
                                    'coordinates': arrCoordinates
                                    ,'crs': {
                                        'type':'name',
                                        'properties': {
                                            'name': 'urn:ogc:def:crs:EPSG::4326'
                                        }
                                    }
                                },
                            }
                            urlS = url_api_instances_const+str(enterprise_sentinel_instance)
                            reponses = requests.request("PUT", urlS, headers=hed, data = json.dumps(data))
                        except Exception as Error:
                            print(str(Error))
                            # log purpuse
                            contextLogs = {
                                'user_email': request.user,
                                'message': 'Fallo PUT sentinel request /parcelasImportFromFileKML',
                                'status': 'error',
                                'extra_data': {
                                    'enterprise_id': str(enterprise_id),
                                    'error': str(Error),
                                    'data': data,
                                    'hed': hed
                                }
                            }
                            ##savelog(contextLogs,request)
                            # end log purpuse
                        
            
            # log purpuse
            contextLogs = {
                'user_email': request.user,
                'message': 'Parcelas procesadas /parcelasImportFromFileKML',
                'status': 'success',
                'extra_data': {
                    "totalparcelas": len(arrToCompare), "cambiadas":len(arrCambiaPoligono)
                }
            }
            ##savelog(contextLogs,request)
            # end log purpuse
            return Response({"procesadas": arrProcesadas, "Overlaps": arrOverlaps, "totalparcelas": len(arrToCompare), "cambiadas": arrCambiaPoligono}, status=status.HTTP_200_OK)
        
        # log purpuse
        contextLogs = {
            'user_email': request.user,
            'message': 'No se puede procesar en /parcelasImportFromFileKML',
            'status': 'warning',
            'extra_data': {
            }
        }
        ##savelog(contextLogs,request)
        # end log purpuse
        return Response({"procesadas": "No se puede procesar", "Overlaps": "No se puede procesar", "totalparcelas": "No se puede procesar"}, status=status.HTTP_400_BAD_REQUEST)

class cargarGeoJsonBBDD(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    """
    # Conectar a la base de datos PostgreSQL
    conn = psycopg2.connect(database="dataforsmartfarming", user="dataforsmartfarmingbackend", password="Cm&O8nOlKZlb", host="localhost", port="5432")

    # Crear un cursor para ejecutar consultas SQL
    cur = conn.cursor()

    # Recorrer todos los archivos GeoJSON en la carpeta "datos" y ejecutar una consulta SQL para cada archivo
    for filename in os.listdir("D:\\ProyectosSMB\\backend\\datos"):
        if filename.endswith(".geojson"):
            with open(os.path.join("D:\\ProyectosSMB\\backend\\datos", filename)) as f:
                # Leer el contenido del archivo GeoJSON y convertirlo en un objeto Python
                data = json.load(f)
                # Recorrer todos los objetos de geometría en el archivo GeoJSON y ejecutar una consulta SQL para cada objeto
                for feature in data["features"]:
                    # Obtener todas las propiedades del objeto de geometría
                    filename = filename
                    empresaImp = "0eacaba3-01ff-47ea-9121-ea76b55e046f"
                    usuarioImp = "5d30e094-da02-4e86-9522-ccea1e2e2e05"
                    sigpac = ""  #feature["properties"]["idPanel"]
                    geometry = json.dumps(feature["geometry"])
                    # Ejecutar una consulta SQL que inserte todas las propiedades en la tabla "mi_tabla"
                    #cur.execute("INSERT INTO mi_tabla (name, description, polygon, polygon_init, enterprise_id, user_created, sigpac_importado, area, date_created, date_updated, user_updated) VALUES (%s, %s, ST_GeomFromGeoJSON(%s), ST_GeomFromGeoJSON(%s), %s, %s, %s, 1, now(), now(), %s)", (filename, filename, geometry, geometry, empresaImp, usuarioImp, sigpac, usuarioImp))

    # Confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    """

class ParcelViewSetNoAuth(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    serializer_class = ParcelSerializer
    model = Parcel

    def get(self, request):
        # todo se agrego para no consumir recursos de sentinel
        parcelas =  Parcel.objects.filter(enterprise__is_monitor=True)
        enterprise_id = request.data['enterprise_id']
        parcels = request.data['parcels']
        # D4SF-88
        continent = request.GET.get("continent", False)
        
        if enterprise_id:
            parcelas = Parcel.objects.filter(enterprise_id=enterprise_id,enterprise__is_monitor=True)
        if enterprise_id and parcels:
            print("parcels",parcels)
            parcelas = Parcel.objects.filter(enterprise_id=enterprise_id, id__in=parcels,enterprise__is_monitor=True)
            print("enterprise_id and parcels")
        # D4SF-88
        if continent:
            print("continent: ", continent)
            parcelas = Parcel.objects.filter(enterprise__continent=continent)

        data = []
        print("cantidad parcelas: ", len(parcelas))
        for parcela in parcelas:
            nombreParcela = parcela.name
            polygon = GEOSGeometry(parcela.polygon)
            geometry_string = polygon.wkt
            area = parcela.area
            polygon.transform(4326)
            bbox = BBox(bbox=polygon.extent, crs=CRS.WGS84)
            data.append({"id": parcela.id, "name": nombreParcela, "geometry_string": geometry_string, "area": area, "bbox": bbox, "polygon.extent": polygon.extent})
        return Response({"data": data}, status=status.HTTP_200_OK)

class ParcelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    model = Parcel

    def get_queryset(self):
        return Parcel.objects.all()

class ParcelViewSetPutPolygon(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    model = Parcel

    def update(self, request, pk=None):
        area = GEOSGeometry(request.data['polygon']).area
        area2 = request.data['area']
        name = request.data['name']
        description = request.data['description']
        areaRound = decimal.Context(prec=3).create_decimal(float(str(area)[:10]))

        # set for loogin purpose
        requestUser = get_request()
        contextLogs = {
            'user_email': requestUser.user,
            'message': '',
            'status': '',
            'extra_data': {
                'parcelaId': pk,
                'name': name,
                'description': description,
                'area':area,
                'polygon': request.data['polygon']
            }
        }    
        

        if area2 == 0:
            if Parcel.objects.filter(id=int(pk)).update(polygon=request.data['polygon'], name=name, description=description):
                parcelaObj = Parcel.objects.filter(id=int(pk)).first()
                enterprise = parcelaObj.__dict__['enterprise_id']  # Obtenemos la empresa
                # set for loogin purpose
                contextLogs['message'] = "Parcela actualizada #1"
                contextLogs['status'] = "success"
                savelog(contextLogs,requestUser)
                return Response({"data": 'OK', "enterprise": enterprise})
            else:
                # set for loogin purpose
                contextLogs['message'] = "Parcela no actualizada #1"
                contextLogs['status'] = "Error"
                savelog(contextLogs,requestUser)
                return Response({"data": "error"})
        else:
            if Parcel.objects.filter(id=int(pk)).update(polygon=request.data['polygon'], area=area2, name=name, description=description):
                parcelaObj = Parcel.objects.filter(id=int(pk)).first()
                enterprise = parcelaObj.__dict__['enterprise_id']  # Obtenemos la empresa
                # set for loogin purpose
                contextLogs['message'] = "Parcela actualizada #2"
                contextLogs['status'] = "success"
                savelog(contextLogs,requestUser)
                return Response({"data": 'OK', "enterprise": enterprise})
            else:
                # set for loogin purpose
                contextLogs['message'] = "Parcela no actualizada #2"
                contextLogs['status'] = "Error"
                savelog(contextLogs,requestUser)
                return Response({"data": "error"})

class ParcelViewSetFiltered(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel
    serializer_class = ParcelSerializerFilter

    def get_queryset(self):
        enterprise_id = self.kwargs['enterprise_id']
        return Parcel.objects.filter(enterprise_id=enterprise_id)


class ParcelViewSetFilterPolygon(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel
    serializer_class = ParcelSerializerFilter

    def get_queryset(self):
        #geom = self.kwargs['geom']
        polygon = self.request.query_params.get('polygon')
        enterprise_id = self.request.query_params.get('enterprise_id')
        return Parcel.objects.filter(polygon__overlaps=polygon, enterprise_id=enterprise_id)

class ParcelViewSetToJSON(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializerFilter
    model = Parcel

    def get(self, request):
        response = serialize('geojson', Parcel.objects.all(), geometry_field='polygon', fields=('enterprise_id', 'pk', 'name', 'description', 'area',))
        return HttpResponse(response)

class ParcelViewSetValidPolygon(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializerFilter
    model = Parcel

    def get(self, request):
        polygon = self.request.query_params.get('polygon')
        return HttpResponse(GEOSGeometry(polygon).simple)

class ParcelViewSetFilteredName(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = Parcel
    serializer_class = ParcelSerializerFilter

    def get_queryset(self):
        queryset = Parcel.objects.all()
        enterprise_id = self.request.query_params.get('enterprise_id')
        search_param = self.request.query_params.get('parcel_mame')
        if search_param:
            queryset = Parcel.objects.filter(enterprise_id=enterprise_id, name__icontains=search_param)
        else:
            queryset = Parcel.objects.filter(enterprise_id=enterprise_id)
        return queryset

class SigpacViewset(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset= Parcel.objects.all
    serializer_class = ParcelSerializerFilterNoSentInstance

    @action(detail=False, methods=['get'])
    def get_comunidades(self, request, *args, **kwargs):
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/comunidades.geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})

    @action(detail=False, methods=['get'])        
    def get_provincias(self, request, *args, **kwargs):
        comunidad = self.request.query_params.get('comunidad')
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/provincias/"+comunidad+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})

    @action(detail=False, methods=['get'])        
    def get_municipios(self, request, *args, **kwargs):
        provincia = self.request.query_params.get('provincia')
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/municipios/"+provincia+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})

    @action(detail=False, methods=['get'])        
    def get_agregados(self, request, *args, **kwargs):
        provincia = self.request.query_params.get('provincia')
        municipio = self.request.query_params.get('municipio')
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/agregados/"+provincia+"/"+municipio+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})

    @action(detail=False, methods=['get'])        
    def get_zonas(self, request, *args, **kwargs):
        provincia = self.request.query_params.get('provincia')
        municipio = self.request.query_params.get('municipio')
        agregado = self.request.query_params.get('agregado')
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/zonas/"+provincia+"/"+municipio+"/"+agregado+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})

    @action(detail=False, methods=['get'])        
    def get_poligonos(self, request, *args, **kwargs):
        provincia = self.request.query_params.get('provincia')
        municipio = self.request.query_params.get('municipio')
        agregado = self.request.query_params.get('agregado')
        zona = self.request.query_params.get('zona')
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/poligonos/"+provincia+"/"+municipio+"/"+agregado+"/"+zona+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})
    
    @action(detail=False, methods=['get'])        
    def get_parcelas(self, request, *args, **kwargs):
        provincia = self.request.query_params.get('provincia')
        municipio = self.request.query_params.get('municipio')
        agregado = self.request.query_params.get('agregado')
        zona = self.request.query_params.get('zona')
        poligono = self.request.query_params.get('poligono')
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/parcelas/"+provincia+"/"+municipio+"/"+agregado+"/"+zona+"/"+poligono+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})

    @action(detail=False, methods=['get'])        
    def get_recintos(self, request, *args, **kwargs):
        provincia = self.request.query_params.get('provincia')
        municipio = self.request.query_params.get('municipio')
        agregado = self.request.query_params.get('agregado')
        zona = self.request.query_params.get('zona')
        poligono = self.request.query_params.get('poligono')
        parcela = self.request.query_params.get('parcela')
        url = "https://sigpac.mapa.es/fega/ServiciosVisorSigpac/query/recintos/"+provincia+"/"+municipio+"/"+agregado+"/"+zona+"/"+poligono+"/"+parcela+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})
    
    @action(detail=False, methods=['get'])        
    def get_direct(self, request, *args, **kwargs):
        dato = self.request.query_params.get('dato')
        url = "https://sigpac.mapa.gob.es/fega/ServiciosVisorSigpac/query/"+dato+".geojson"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data=response.json()
        return Response({"data": data})