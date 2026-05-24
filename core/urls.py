from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # подключаем наше приложение
    path('orders/', include('orders.urls')),
    path('', home, name='home'),
    
]