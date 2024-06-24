from rest_framework import routers
from django.conf.urls import url

from .viewsets import ImagenProViewSet, ImagenProViewSetAll, ImagenProViewSetTypeTwo, ImagenProViewSetUnificar

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register('ver_hist', ImagenProViewSetAll)

urlpatterns = [
    url(r'^procesado/', ImagenProViewSet.as_view()),
    url(r'^procesadot2/', ImagenProViewSetTypeTwo.as_view()),
    url(r'^unificarInforme/', ImagenProViewSetUnificar.as_view()),
]

urlpatterns += router.urls