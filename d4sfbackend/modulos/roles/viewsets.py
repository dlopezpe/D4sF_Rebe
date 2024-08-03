from rest_framework import viewsets

from .models import Rol
from .serializer import RolSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class RolViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Rol.objects.all()
    serializer_class = RolSerializer