from rest_framework import routers

from .viewsets import ParcelViewSet

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register('parcels', ParcelViewSet)

urlpatterns = router.urls