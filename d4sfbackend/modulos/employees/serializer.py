from rest_framework import serializers

from modulos.employees.models import Employee
from modulos.roles.serializer import RolSerializer
from modulos.groups.serializer import GroupSerializer
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class EmployeeSerialiser(serializers.ModelSerializer):
    roles = RolSerializer(many=True, required=False)
    groups = GroupSerializer(many=True, required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Dejar en blanco si no se necesita cambio',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    hasRoles = serializers.BooleanField(required=False, default=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'hasRoles', 'email', 'phone', 'password', 'roles', 'groups')

    def __init__(self, *args, **kwargs):
        super(EmployeeSerialiser, self).__init__(*args, **kwargs)
        self.fields["name"].error_messages["required"] = u"El Nombre es un campo requerido"
        self.fields["name"].error_messages["blank"] = u"El Nombre no puede estar en blanco"
        self.fields["email"].error_messages["required"] = u"El Email es requerido"
        self.fields["email"].error_messages["blank"] = u"El Email no puede estar en blanco"
