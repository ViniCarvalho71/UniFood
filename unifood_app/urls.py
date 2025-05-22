from django.urls import path
from .views import usuario, pedidos

urlpatterns = [
    path('login/', usuario.Login, name="login"),
    path('registrar/', usuario.Registrar, name="registrar"),
    path('logout/', usuario.Logout, name="logout"),
    path('pedido/listar', pedidos.lista_pedidos, name="listar")

]