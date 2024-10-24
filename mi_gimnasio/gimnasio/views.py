from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status, generics


'''
Comandos para auth:
    Registro:
        curl -X POST -H "Content-Type: application/json" -d '{
          "username": "newuser",
          "password": "newpassword123",
          "email": "newuser@example.com",
          "first_name": "FirstName",
          "last_name": "LastName"
        }' http://localhost:8000/app/register/

    Login:
        curl   -X POST   -H "Content-Type: application/json"   -d '{"username": "newuser", "password": "newpassword123"}'   http://localhost:8000/api/token/


    Testear Auth:
    curl -H "Authorization: Bearer INSERTAR_TOKEN_GENERADO_AQUI"   http://localhost:8000/app/test/

    Ejemplo de mensaje de auth exitoso:
{"user":"newuser","auth":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NzQxMjk2LCJpYXQiOjE3Mjk3NDA5OTYsImp0aSI6ImE1MjhmNDI3ZGU4MDRjNjY4NDM3ZGU3NWVkMzg3ZmY1IiwidXNlcl9pZCI6Mn0.39_2bgIYBru3V3LyLc2vkptEES3VULv9KzcX8PLuGUU","message":"Success!"}

'''

class CreateUser(generics.CreateAPIView):
    permisson_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExampleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
            'message': 'Success!'
        }
        return Response(content)
# Create your views here.:
