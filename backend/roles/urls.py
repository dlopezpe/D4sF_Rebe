from rest_framework import routers

from .viewsets import RolViewSet

router = routers.SimpleRouter()
router.register('roles', RolViewSet)

urlpatterns = router.urls