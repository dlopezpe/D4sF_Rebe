from rest_framework import routers

from .viewsets import EnterpriseViewSet, EnterpriseViewSetCount, EnterpriseViewSetExcept, EnterpriseViewSetActive, EnterpriseViewSetActiveAndMonitor

router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register('enterprises', EnterpriseViewSet)
router.register('enterprises_except', EnterpriseViewSetExcept)
router.register('enterprises_count', EnterpriseViewSetCount)
router.register('enterprises_active', EnterpriseViewSetActive)
router.register('enterprises_active_and_monitor', EnterpriseViewSetActiveAndMonitor)

urlpatterns = router.urls