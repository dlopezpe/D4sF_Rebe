from rest_framework import routers
from django.conf.urls import url

from newimgprocess import viewsets
from .viewsets import NewImagenProViewSet, NewImagenProFechasViewSet, NewImagenProUnificarViewSet, NewImagenProGetBBoxViewSet, GenerarExcelViewSet

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register(r'generarinforme', viewsets.GenerarExcelViewSet, basename='generarinforme')
#router.register('ver_hist', ImagenProViewSetAll)

urlpatterns = [
    url(r'^procesadonew/', NewImagenProViewSet.as_view()),
    url(r'^procesadonewfechas/', NewImagenProFechasViewSet.as_view()),
    url(r'^unificarInformes/', NewImagenProUnificarViewSet.as_view()),
    url(r'^getbbox/', NewImagenProGetBBoxViewSet.as_view())
]

urlpatterns += router.urls