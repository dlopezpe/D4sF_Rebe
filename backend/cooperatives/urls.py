from rest_framework import routers
from django.conf.urls import url

from .viewsets import CooperativeViewset, CooperativeInsViewset, CooperativeViewsetOnEnRlt, CooperativeViewsetUpdate

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register('cooperatives', CooperativeViewset)
router.register('cooperativesr', CooperativeViewsetUpdate)
router.register('cooperativesonenrlt', CooperativeViewsetOnEnRlt)

urlpatterns = [
    url(r'^cooperativess/', CooperativeInsViewset.as_view()),
]

urlpatterns += router.urls