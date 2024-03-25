"""
URL configuration for djangoProject_ProjetModule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# urls.py
from django.urls import path
from . import views
from .views import get_devices, fetch_ir_codes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('add_device', views.add_device, name='add_device'),
    path('get-devices/<int:user_id>/', get_devices, name='get_devices'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('store-ir-codes/', views.store_ir_codes, name='store_ir_codes'),
    path('fetch-ir-codes/<str:device_id>/', fetch_ir_codes, name='fetch_ir_codes'),
]

