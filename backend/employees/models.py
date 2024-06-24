import uuid
from django.db import models
from roles.models import Rol
from groups.models import Group
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=254)
    hasRoles = models.BooleanField()
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    roles = models.ManyToManyField(Rol)
    groups = models.ManyToManyField(Group)

    
