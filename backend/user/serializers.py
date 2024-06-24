from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from profiles.models import UserProfile
from .models import User


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        #fields = ('id', 'first_name', 'last_name', 'phone_number', 'user', 'permisos')
        fields = ('__all__')


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'is_enterpriseadmin', 'language', 'profile')
        extra_kwargs = {'password': {'write_only': True, 'required': False, 'allow_blank': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            phone_number=profile_data['phone_number'],
            enterprise_id=profile_data['enterprise_id'],
            cooperative_user=profile_data['cooperative_user'],
        )
        return user

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }

class UserSerializerPer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'is_enterpriseadmin', 'is_systemadmin', 'language')

class UserSerializerData(serializers.ModelSerializer):
    password = serializers.CharField(required = False)
    class Meta:
        model = User
        fields = ('id', 'email', 'is_enterpriseadmin', 'is_staff', 'password', 'last_login', 'language')
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

"""
class UserSerializerRecoverPass(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data.get("email", None)
        print(email)
        user = authenticate(email=email)
        if user is None:
            raise serializers.ValidationError(
                'No se encuentra un usuario con este correo electrónico.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }
"""

class CustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField(required = False)
    token = serializers.CharField()
    type = 'reset'