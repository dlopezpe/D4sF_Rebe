from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ndvimonitor import views as ndvimonitor_views

from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'ndvimonitor', ndvimonitor_views.NdviMonitorViewSet, basename='ndvimonitor')

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)