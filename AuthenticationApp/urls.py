"""Campus_Forum URL Configuration

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

from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('register', views.user_registration, name="User-Registration"),
    path('reset_password', views.reset_password, name="Password-Reset"),
    path('reset_password_request', views.email_reset_link, name="Password-Reset-Link"),
    path('activate/<uidb64>/<token>', views.activate_user, name="Activate-Account"),
    path('user/<str:username>', views.user_profile, name="Current-User-Details"),
    path('user/', views.profile, name="Current-User-Details"),
    path('update/user_image', views.update_user_image, name="Update-User-Image"),
    path('csrf/', views.csrf_token_generator, name="CSRF-Token")
]
