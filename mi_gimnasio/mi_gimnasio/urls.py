
''' 
Se importa simple JsonWebToken a lao urls
para la autentiacion.
'''
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from gimnasio.views import CreateUser
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUser.as_view(), name="register"),
    path('app/', include('gimnasio.urls')),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls')),
]
