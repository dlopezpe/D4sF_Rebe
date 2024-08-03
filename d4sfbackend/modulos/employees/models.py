from django.db import models

from modulos.groups.models import Group
from modulos.roles.models import Rol


# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=254)
    hasRoles = models.BooleanField()
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    roles = models.ManyToManyField(Rol)
    groups = models.ManyToManyField(Group)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'employees'

    def __str__(self):
        return self.name

    
