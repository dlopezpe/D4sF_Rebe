from rest_framework import viewsets
from .models import Employee
from .serializer import EmployeeSerialiser


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerialiser
