from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import status, generics
from .models import Cliente, Instructor, Pago, Clase, Membresia, Asistencia, Factura
from datetime import date
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
        }' http://localhost:8000/api/register/

    Login:
        curl   -X POST   -H "Content-Type: application/json"   -d '{"username": "newuser", "password": "newpassword123"}'   http://localhost:8000/api/token/


    Testear Auth:
    curl -H "Authorization: Bearer INSERTAR_TOKEN_GENERADO_AQUI"   http://localhost:8000/api/home/

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

class perfil_cliente(APIView):
    """
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNjQ1NDgzLCJpYXQiOjE3MzMyNDk0ODMsImp0aSI6IjVmODJjNjAzZjU1YjQ1YTE5ZDE2M2QwYTYxMGRmYWIzIiwidXNlcl9pZCI6Mn0.135FqyOayr7p6fiLdk9lMpmxpQ0uJhl9NoQFTp2fe7Q"   http://localhost:8000/api/perfil/
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        cliente = user.cliente
        
        asistencias = Asistencia.objects.filter(cliente=cliente).select_related('clase') 
        attendance_history = [
            {
                'clase_nombre': asistencia.clase.nombre_clase,  # Assuming Clase model has a 'nombre' field
            } for asistencia in asistencias
        ]
        
        content = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'cliente': {
                'telefono': cliente.telefono,
                'direccion': cliente.direccion,
            },
            'attendance_history': attendance_history
        }
        
        return Response(content)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class RegisterForClass(generics.CreateAPIView):

    """
curl -X POST \
     -H "Authorization: Bearer TOKEN_AQUI" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/registrar_asistencia/id/post/

    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_id = self.kwargs.get('class_id')
        class_obj = Clase.objects.get(id=class_id)
        user_id = request.user.id
        cliente = User.objects.get(id=user_id)
        Asistencia.objects.create(
            clase=class_obj,
            cliente=cliente.cliente
        )
        return Response({"message": "Registered successfully"}, status=status.HTTP_201_CREATED)


class ListClasses(APIView):
    """
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNjQ1NDgzLCJpYXQiOjE3MzMyNDk0ODMsImp0aSI6IjVmODJjNjAzZjU1YjQ1YTE5ZDE2M2QwYTYxMGRmYWIzIiwidXNlcl9pZCI6Mn0.135FqyOayr7p6fiLdk9lMpmxpQ0uJhl9NoQFTp2fe7Q"   http://localhost:8000/api/clases/
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        class_obj = Clase.objects.filter(fecha_clase__gt=date.today())
        serialized_data = ClaseSerializer(class_obj, many=True).data

        return Response({"clases": serialized_data})
        
class CreateClass(APIView):

    """
     curl -X POST      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzIwNjU0LCJpYXQiOjE3MzMzMjQ2NTQsImp0aSI6IjI4ZTU3OTVmMjcxMjRhYzA4ZTQ5NDQyYmJkY2JlM2RhIiwidXNlcl9pZCI6Mn0.GKSpM56JsNSXSAYMNyVU1GY27YkoUn7dJeJJrDh6JsY"      -H "Content-Type: application/json"      -d '{
         "nombre_clase": "Yoga Basics",
         "descripcion": "An introductory yoga class for beginners.",
         "fecha_clase": "2024-12-15",
         "hora_inicio": "10:00:00",
         "hora_fin": "11:30:00",
         "instructor_id": 1
     }'      http://localhost:8000/api/clases/crear/
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            data = request.data
            instructor_id = data.get("instructor_id")

            # Ensure the instructor exists
            instructor = Instructor.objects.get(id=instructor_id)

            # Create a new Clase object
            clase = Clase.objects.create(
                nombre_clase=data.get("nombre_clase"),
                descripcion=data.get("descripcion"),
                fecha_clase=data.get("fecha_clase"),
                hora_inicio=data.get("hora_inicio"),
                hora_fin=data.get("hora_fin"),
                instructor=instructor
            )

            # Serialize and return success response
            return Response({
                "message": "Clase created successfully",
                "id": clase.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
