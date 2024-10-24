from django.contrib.auth.models import User
from .models import Cliente,Instructor, Pago, Clase, Membresia, Asistencia, Factura
from rest_framework import serializers

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['telefono', 'direccion']
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'
class PagoSerializer(serializers.ModelSerializer):
    #cliente = ClienteSerializer()
    class Meta:
        model = Pago
        fields = '__all__'
class MembresiaSerializer(serializers.ModelSerializer):
    #cliente = ClienteSerializer()
    class Meta:
        model = Membresia
        fields = '__all__'
class ClaseSerializer(serializers.ModelSerializer):
   # instructor = InstructorSerializer()
    class Meta:
        model = Clase
        fields = '__all__'
class AsistenciaSerializer(serializers.ModelSerializer):
 #   cliente = ClienteSerializer()
  #  clase = ClaseSerializer()
    class Meta:
        model = Asistencia
        fields = '__all__'
class FacturaSerializer(serializers.ModelSerializer):
#    cliente = ClienteSerializer()
    class Meta:
        model = Factura
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
 #   cliente  = ClienteSerializer()
#    instructor = InstructorSerializer()
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

