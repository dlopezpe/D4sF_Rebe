from .models import Cooperative
from rest_framework import serializers
from enterprises.serializer import EnterpriseSerializer

class CooperativeSerializer(serializers.ModelSerializer):
    id_empresas = serializers.ListField(child=serializers.CharField(read_only=True), required = False, read_only=True)
    name = serializers.CharField(required = False)
    enterprises = EnterpriseSerializer(many=True, required = False)
    
    #Filtramos solo las enterprises con is_active=True
    
    class Meta:
        model = Cooperative
        fields = ('id', 'name', 'direction', 'phone_number', 'cif', 'is_active', 'id_empresas', 'enterprises')


class CooperativeSerializerOnlyEnterprisesRelated(serializers.ModelSerializer):
    enterprises = EnterpriseSerializer(many=True, required = False)
    class Meta:
        model = Cooperative
        fields = ('id', 'name', 'direction', 'phone_number', 'cif', 'is_active', 'enterprises')

class CooperativeSerializerRR(serializers.ModelSerializer):
    id_empresas = serializers.ListField(child=serializers.CharField(read_only=True), required = False, read_only=True)
    name = serializers.CharField(required = False)
    class Meta:
        model = Cooperative
        fields = ('id', 'name', 'direction', 'phone_number', 'cif', 'is_active', 'id_empresas', 'enterprises')
    