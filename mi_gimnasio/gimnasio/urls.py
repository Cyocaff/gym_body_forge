from django.urls import path, include
from rest_framework import routers
from . import views 

#router = routers.DefaultRouter()
#router.register(r'', views. ,'')

urlpatterns=[
        #   path('api/', include (router.urls)),
    path('test/', views.ExampleView.as_view()),
    path('register/', views.RegisterView.as_view(), name='register'),
    ]
