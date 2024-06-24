from rest_framework import routers

from .viewsets import GroupViewSet

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register('groups', GroupViewSet)

urlpatterns = router.urls