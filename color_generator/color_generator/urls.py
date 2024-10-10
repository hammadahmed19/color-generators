"""
URL configuration for color_generator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import create_colour_scheme , get_colour_schemes_and_name , update_colour_scheme , delete_colour_scheme
from myapp.views import RegisterView , LoginView , LogoutView
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', create_colour_scheme, name='create_colour_scheme'),
    path('get/', get_colour_schemes_and_name, name='get_colour_'),
    path('update/<int:pk>/', update_colour_scheme, name='update_colour_scheme'),
    path('delete/<int:pk>/', delete_colour_scheme, name='delete_colour_scheme'),
    path('api/auth/register/', RegisterView.as_view(), name='auth-register'),
    path('api/auth/login/', LoginView.as_view(), name='auth-login'),  
    path('api/auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
