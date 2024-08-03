from rest_framework import routers
from django.urls import re_path as url
from django.urls import include, path

from modulos.campanas import viewsets
from .viewsets import ImportCampanaFromFileViewset

router = routers.SimpleRouter()  # Clase que de Define un CRUD de nuestro modelo
router.register(r'campana', viewsets.Campanaviewset, basename='campana')
router.register(r'siembra', viewsets.Siembraviewset, basename='siembra')
router.register(r'produccion', viewsets.Produccionviewset, basename='produccion')

urlpatterns = [
    url(r'^campanaImportFromFile/', ImportCampanaFromFileViewset.as_view()),
    path('', include(router.urls))
]

urlpatterns += router.urls
