
from .views import UserProfileView, ProfilesView
from .viewsets import ProfilesViewSet, ProfileViewSet, ProfileViewSetPer, ProfilesViewSetFiltered, ProfileViewSetData, ProfilesViewSetFilteredUser
from rest_framework import routers
from django.conf.urls import url

"""
urlpatterns = [
    url(r'^profile', UserProfileView.as_view()),
    url(r'^perfiles', ProfilesView),
    url(r'^perfiles/perfilestodos', ProfilesViewSet)
]
"""
router = routers.SimpleRouter() # Clase que de Define un CRUD de nuestro modelo
router.register(r'profile', ProfileViewSet, basename='Perfil')
router.register(r'profiles', ProfilesView, basename='Perfiles')
router.register(r'permisos', ProfileViewSetPer, basename='PerfilesRoles')
router.register(r'profiledata', ProfileViewSetData, basename='PerfilesData')



urlpatterns = [
    url(r'^profiles_enterprises/(?P<enterprise_id>.+)/$', ProfilesViewSetFiltered.as_view()),
    url(r'^profiles_filter/(?P<user_id>.+)/$', ProfilesViewSetFilteredUser.as_view())
]

urlpatterns += router.urls