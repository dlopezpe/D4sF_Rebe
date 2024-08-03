from rest_framework import routers
from django.urls import re_path as url


from .viewsets import ImportParcelsFromFileKMLViewset,ImportParcelsFromGeoJSONViewset, ImportParcelsFromFileViewset, ParcelViewSetNoAuth, ParcelViewSet, ParcelViewSetFiltered, ParcelViewSetFilterPolygon, ParcelViewSetToJSON, ParcelViewSetValidPolygon, ParcelViewSetFilteredName, ParcelViewSetPutPolygon, cargarGeoJsonBBDD, SigpacViewset

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register('parcels', ParcelViewSet)
router.register('parcel', ParcelViewSetPutPolygon)
router.register(r'sigpac', SigpacViewset, basename='sigpac')

urlpatterns = [
    url(r'^parcel_enterprise/(?P<enterprise_id>.+)/$', ParcelViewSetFiltered.as_view()),
    url(r'^parcel_filter/', ParcelViewSetFilterPolygon.as_view()),
    url(r'^parcels_json/', ParcelViewSetToJSON.as_view()),
    url(r'^parcel_valid/', ParcelViewSetValidPolygon.as_view()),
    url(r'^parcel_filtername/', ParcelViewSetFilteredName.as_view()),
    url(r'^parcelasNoAuth/', ParcelViewSetNoAuth.as_view()),
    url(r'^parcelasImportFromFile/', ImportParcelsFromFileViewset.as_view()),
    url(r'^parcelasImportFromFileKML/', ImportParcelsFromFileKMLViewset.as_view()), 
    url(r'^parcelasImportFromGeoJSON/', ImportParcelsFromGeoJSONViewset.as_view()), 
    url(r'^cargarGeoJsonBBDD/', cargarGeoJsonBBDD.as_view()),
    #url(r'^sigpac/', SigpacViewset.as_view()),
]

urlpatterns += router.urls
