from django.contrib import admin
from .models import Instructor,Cliente,Clase,Membresia,Factura,Asistencia,Pago


# Register your models here.

admin.site.register(Instructor)
admin.site.register(Cliente)
admin.site.register(Clase)
admin.site.register(Membresia)
admin.site.register(Factura)
admin.site.register(Asistencia)
admin.site.register(Pago)
