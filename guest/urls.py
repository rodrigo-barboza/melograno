"""melograno URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('sauth/', include('social_django.urls', namespace='melograno')),
    path('auth/login', views.user_login, name='user_login'),
    path('auth/login/google', views.user_google_login, name='user_google_login'),
    path('auth/logout', views.user_logout, name='user_logout'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('home', views.home, name='home'),
    path('', include('social_django.urls', namespace='melograno')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="guest/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="guest/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="guest/new_password.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="guest/password_reset_complete.html"), name="password_reset_complete"),
]
