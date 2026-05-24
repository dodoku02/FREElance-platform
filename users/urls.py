from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]