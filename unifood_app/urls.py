from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuario.homeView, name="home")
]