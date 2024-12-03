from django.db import models
from django.contrib.auth.models import User
class Cliente(models.Model):
    usuario = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)


class Instructor(models.Model):
    usuario = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_contratacion = models.DateField()

class Clase(models.Model):
    nombre_clase = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_clase = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)


class Membresia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_membresia = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField()
    descripcion = models.TextField()


class Pago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    metodo_pago = models.CharField(max_length=50)
    estado_pago = models.CharField(max_length=20)

class Asistencia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    detalles_factura = models.TextField()
