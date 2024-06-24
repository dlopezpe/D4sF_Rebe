from rest_framework import viewsets

from .models import Parcel
from .serializer import ParcelSerializer

class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer