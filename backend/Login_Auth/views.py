from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from .models import *
from knox.models import AuthToken
from django.contrib.auth import get_user_model,authenticate
User = get_user_model()


class RegisterViewset(viewsets.ViewSet):  
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user :
                _, token = AuthToken.objects.create(user)
                return Response({
                    "message": "Login successful",
                    "user": self.serializer_class(user).data,  # <-- Correct
                    "token": token
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewset(viewsets.ViewSet):  
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def list(self, request):
        queryset=User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)