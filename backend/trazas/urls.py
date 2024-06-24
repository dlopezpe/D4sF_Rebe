from rest_framework import routers

from .viewsets import TrazasViewSet

router = routers.SimpleRouter()
router.register('insert_trazas', TrazasViewSet, basename="insert_trazas")
router.register('insert_trazas_enterprise', TrazasViewSet, basename="insert_trazas_enterprise")


urlpatterns = router.urls