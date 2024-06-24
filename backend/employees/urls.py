from rest_framework import routers

from .viewsets import EmployeeViewSet

router = routers.SimpleRouter()
router.register('employees', EmployeeViewSet)

urlpatterns = router.urls