from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import status, generics
from .models import Cliente, Instructor, Pago, Clase, Membresia, Asistencia, Factura
from .serializers import (
    UserSerializer, ClienteSerializer, InstructorSerializer, 
    PagoSerializer, MembresiaSerializer, ClaseSerializer, 
    AsistenciaSerializer, FacturaSerializer
)


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
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# View to List and Create Clientes
class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny]

# View to List and Create Instructors
class InstructorListCreateView(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]

# View to List and Create Pagos
class PagoListCreateView(generics.ListCreateAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [AllowAny]

# View to List and Create Membresias
class MembresiaListCreateView(generics.ListCreateAPIView):
    queryset = Membresia.objects.all()
    serializer_class = MembresiaSerializer
    permission_classes = [AllowAny]

# View to List and Create Clases
class ClaseListCreateView(generics.ListCreateAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer
    permission_classes = [AllowAny]

# View to List and Create Asistencias
class AsistenciaListCreateView(generics.ListCreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [AllowAny]

# View to List and Create Facturas
class FacturaListCreateView(generics.ListCreateAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [AllowAny]
