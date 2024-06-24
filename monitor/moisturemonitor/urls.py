from django.urls import include, path
from rest_framework.routers import DefaultRouter
from moisturemonitor import views as moisturemonitor_views

from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'moisturemonitor', moisturemonitor_views.NdviMonitorViewSet, basename='moisturemonitor')

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)