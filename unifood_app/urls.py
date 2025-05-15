from django.urls import path
from .views import usuario

urlpatterns = [
    path('login/', usuario.Login, name="home"),
    path('registrar/', usuario.Registrar, name="registrar"),

]