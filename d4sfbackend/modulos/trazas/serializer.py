from .models import Trazas
from rest_framework import serializers


class TrazasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trazas
        fields = '__all__'