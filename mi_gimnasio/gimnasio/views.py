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
Por motivos de testeo se ha incluido un comand curl http por cada endpoint usable.
En algunos comandon hay que reemplazar el token y el id.
Los comandos para obtener es token se muestran mas abajo.
Para cambiar la duracion y parametros leer la documentacion de JWT,
los settings estan en settings.py.
'''

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
        curl   -X POST   -H "Content-Type: application/json"   -d '{"username": "newuser", "password": "newpassword123"}'   http://localhost:8000/auth/login/


    Testear Auth:
    curl -H "Authorization: Bearer INSERTAR_TOKEN_GENERADO_AQUI"   http://localhost:8000/api/home/

    Ejemplo de mensaje de auth exitoso:
{"user":"newuser","auth":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NzQxMjk2LCJpYXQiOjE3Mjk3NDA5OTYsImp0aSI6ImE1MjhmNDI3ZGU4MDRjNjY4NDM3ZGU3NWVkMzg3ZmY1IiwidXNlcl9pZCI6Mn0.39_2bgIYBru3V3LyLc2vkptEES3VULv9KzcX8PLuGUU","message":"Success!"}

'''

"""
<=======================================>
!!!!!README!!!! LEER AQUI, IMPORTANTE!!!!

Por motivos de seguridad la unica forma de
asignar la tabla 'Cliente' o 'Instructor' 
a un usuario es a traves de el panel de
administracion de Django admin en /admin/
esto para prevenir una escalada de privilegios
mediante ataques maliciosos en URLs
<=======================================>
"""


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
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        try:
            user_object = request.user
            try:
                if user_object.instructor:
                    print("")
            except Exception:
                return Response({"message": "User is not authorized to perform operation"})
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
class GenerarBoleta(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
         curl -X POST      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzIwNjU0LCJpYXQiOjE3MzMzMjQ2NTQsImp0aSI6IjI4ZTU3OTVmMjcxMjRhYzA4ZTQ5NDQyYmJkY2JlM2RhIiwidXNlcl9pZCI6Mn0.GKSpM56JsNSXSAYMNyVU1GY27YkoUn7dJeJJrDh6JsY"      -H "Content-Type: application/json"      -d '{
         "monto": 44500,
         "fecha_pago": "2024-12-11",
         "metodo_pago": "Debito"
     }'      http://localhost:8000/api/registrar_boleta/post/
    """
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user= request.user
            user_cliente = user.cliente
            pago=Pago.objects.create(
                cliente=user_cliente,
                monto=data.get("monto"),
                fecha_pago=data.get("fecha_pago"),
                metodo_pago=data.get("metodo_pago"),
            )

            return Response({
                "message": "Boleta created successfully",
                "id": pago.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class BoletasCliente(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNjQ1NDgzLCJpYXQiOjE3MzMyNDk0ODMsImp0aSI6IjVmODJjNjAzZjU1YjQ1YTE5ZDE2M2QwYTYxMGRmYWIzIiwidXNlcl9pZCI6Mn0.135FqyOayr7p6fiLdk9lMpmxpQ0uJhl9NoQFTp2fe7Q"   http://localhost:8000/api/cuenta/pagos/
    """
    def get(self,request):
        user = request.user
        cliente = user.cliente
        pagos_obj = Pago.objects.filter(cliente=cliente) 
        serialized_data = PagoSerializer(pagos_obj, many=True).data
        return Response({"pagos": serialized_data})
class GenerarMembresia(APIView):
    """
         curl -X POST      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzIwNjU0LCJpYXQiOjE3MzMzMjQ2NTQsImp0aSI6IjI4ZTU3OTVmMjcxMjRhYzA4ZTQ5NDQyYmJkY2JlM2RhIiwidXNlcl9pZCI6Mn0.GKSpM56JsNSXSAYMNyVU1GY27YkoUn7dJeJJrDh6JsY"      -H "Content-Type: application/json"      -d '{
         "pago": 1,
         "tipo_membresia": "Platino",
         "precio": 1000,
         "duracion": 1,
         "descripcion": "Membresia platino mensual"
     }'      http://localhost:8000/api/membresia/post/
    """

    """
    Detalle: Las relaciones de pago - membresia son irrepetibles,
    ademas, en caso de que el monto del pago no sea igual al precio de la
    membresia, no se permitra proceder.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        data = request.data
#        pago_id = self.kwargs.get('pago_id')
        pago_id = data.get("pago")
        pago_obj = Pago.objects.get(id=pago_id)
        if pago_obj.monto != data.get("precio"):
            return Response({"message":"Monto de pago erroneo, por favor contactar a servicio al cliente."})
        membresia=Membresia.objects.create(
            pago=pago_obj,
            tipo_membresia=data.get("tipo_membresia"),
            precio=data.get("precio"),
            duracion=data.get("duracion"),
            descripcion=data.get("descripcion")
            )
        return Response({
            "message": "Boleta created successfully",
            "id": membresia.id
            }, status=status.HTTP_201_CREATED)

class Membresias(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNjQ1NDgzLCJpYXQiOjE3MzMyNDk0ODMsImp0aSI6IjVmODJjNjAzZjU1YjQ1YTE5ZDE2M2QwYTYxMGRmYWIzIiwidXNlcl9pZCI6Mn0.135FqyOayr7p6fiLdk9lMpmxpQ0uJhl9NoQFTp2fe7Q"   http://localhost:8000/api/cuenta/membresias/
    """
    def get(self, request):
        user_obj = request.user
        cliente_obj = user_obj.cliente
        membresias_obj = Membresia.objects.filter(pago__cliente=cliente_obj)
        serialized_data = MembresiaSerializer(membresias_obj, many=True).data
        return Response({"membresias": serialized_data})



class GenerarFactura(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
         curl -X POST      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzIwNjU0LCJpYXQiOjE3MzMzMjQ2NTQsImp0aSI6IjI4ZTU3OTVmMjcxMjRhYzA4ZTQ5NDQyYmJkY2JlM2RhIiwidXNlcl9pZCI6Mn0.GKSpM56JsNSXSAYMNyVU1GY27YkoUn7dJeJJrDh6JsY"      -H "Content-Type: application/json"      -d '{
         "fecha_emision": "2024-12-12",
         "total": 1000,
         "detalles_factura": 1
     }'      http://localhost:8000/api/factura/post/
    """
    def post(self,request,*args,**kwargs):
        data = request.data
        user_obj = request.user
        factura = Factura.objects.create(
                cliente = user_obj.cliente,
                fecha_emision = data.get("fecha_emision"),
                total = data.get("total"),
                detalles_factura = data.get("detalles_factura")
                )
        return Response({"message": "Factura created successfully", "id": factura.id})

class Facturas(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    """
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNjQ1NDgzLCJpYXQiOjE3MzMyNDk0ODMsImp0aSI6IjVmODJjNjAzZjU1YjQ1YTE5ZDE2M2QwYTYxMGRmYWIzIiwidXNlcl9pZCI6Mn0.135FqyOayr7p6fiLdk9lMpmxpQ0uJhl9NoQFTp2fe7Q"   http://localhost:8000/api/cuenta/facturas/
    """
    def get(self,request):
        user_obj = request.user
        cliente = user_obj.cliente
        facturas_obj = Factura.objects.filter(cliente=cliente)
        serialized_data = FacturaSerializer(facturas_obj, many=True).data
        return Response({"pagos": serialized_data})
