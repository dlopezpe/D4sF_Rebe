from django.db import models


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'groups'

    def __str__(self):
        return self.name
