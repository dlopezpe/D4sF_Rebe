"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/', include('employees.urls')),
    path('api/v1.0/', include('roles.urls')),
    path('api/v1.0/', include('groups.urls')),
    path('api/v1.0/', include('parcelas.urls')),
    path('api-token-auth/', obtain_jwt_token, name='api_token_auth'),
    path('api-token-refresh/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('api/v1.0/', include('user.urls')),
    path('api/v1.0/', include('profiles.urls')),
    path('api/v1.0/', include('enterprises.urls')),
    path('api/v1.0/', include('imgprocess.urls')),
    path('api/v1.0/', include('cooperatives.urls')),
    path('api/v1.0/', include('newimgprocess.urls')),
    path('api/v1.0/', include('campanas.urls')),
    path('api/v1.0/', include('trazas.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)