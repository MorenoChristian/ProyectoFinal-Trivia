"""Trivia URL Configuration

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
from django.urls import path
from Provincializacion.views import inicio
from Trivia.views import registro, loginView, logoutView, Home, jugar, resultado_pregunta


urlpatterns = [
    path('admin/', admin.site.urls),
    path("inicio/", inicio, name="inicio"),
    path("home/", Home, name="home"),

    path("registro/",registro),
    path("login/",loginView, name="login"),
    path("logout/", logoutView, name="logout"),
    
    path("jugar/",jugar, name="jugar"),
    path("resultado/ <int:pregunta_respondida_pk>/", resultado_pregunta, name = 'resultado')
]
