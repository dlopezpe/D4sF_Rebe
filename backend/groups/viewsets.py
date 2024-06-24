from rest_framework import viewsets
from .models import Group
from .serializer import GroupSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = Group.objects.all()
    serializer_class = GroupSerializer