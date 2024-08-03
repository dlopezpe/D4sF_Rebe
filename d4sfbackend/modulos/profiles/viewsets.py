from rest_framework import viewsets, generics

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from modulos.user.serializers import UserSerializer, UserSerializerPer, UserSerializerData
from .models import UserProfile
from modulos.user.models import User


class ProfilesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user=user)

class ProfileViewSetPer(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserSerializerPer    

class ProfilesViewSetFiltered(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = UserProfile
    serializer_class = UserSerializer

    def get_queryset(self):
        enterprise_id = self.kwargs['enterprise_id']
        return UserProfile.objects.filter(enterprise_id=enterprise_id)
        
class ProfilesViewSetFilteredUser(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    model = UserProfile
    serializer_class = UserSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return UserProfile.objects.filter(user_id=user_id)

class ProfileViewSetData(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset = User.objects.all()
    serializer_class = UserSerializerData
