from rest_framework import routers
from django.conf.urls import url
from django.urls import include, path

from campanas import viewsets
from .viewsets import ImportCampanaFromFileViewset

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register(r'campana', viewsets.campanaViewSet, basename='campana')
router.register(r'siembra', viewsets.siembraViewSet, basename='siembra')
router.register(r'produccion', viewsets.produccionViewSet, basename='produccion')

urlpatterns = [
    url(r'^campanaImportFromFile/', ImportCampanaFromFileViewset.as_view()),
    path('', include(router.urls))
]

urlpatterns += router.urls
