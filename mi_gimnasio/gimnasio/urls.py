from django.urls import path, include
from rest_framework import routers
from . import views
from .views import (
    UserListCreateView, ClienteListCreateView, InstructorListCreateView,
    PagoListCreateView, MembresiaListCreateView, ClaseListCreateView,
    AsistenciaListCreateView, FacturaListCreateView
)#router = routers.DefaultRouter()
#router.register(r'', views. ,'')

urlpatterns=[
        #   path('api/', include (router.urls)),
    path('home/', views.ExampleView.as_view()),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('instructores/', InstructorListCreateView.as_view(), name='instructor-list-create'),
    path('pagos/', PagoListCreateView.as_view(), name='pago-list-create'),
    path('membresias/', MembresiaListCreateView.as_view(), name='membresia-list-create'),
    path('clases/', ClaseListCreateView.as_view(), name='clase-list-create'),
    path('asistencias/', AsistenciaListCreateView.as_view(), name='asistencia-list-create'),
    path('facturas/', FacturaListCreateView.as_view(), name='factura-list-create'),
    path('perfil/', views.perfil.as_view()),

    path('registrar_asistencia/<int:class_id>/post/', views.RegisterForClass.as_view(), name='register_attendance'),
    ]
