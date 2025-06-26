from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')  # Add 'username'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_representation(self, instance):
        ret= super().to_representation(instance)
        ret.pop('password', None)  # Remove password from the representation
        return ret