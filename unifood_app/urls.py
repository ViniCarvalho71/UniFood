from django.urls import path
from .views import usuario, pedidos, produto

urlpatterns = [
    path('login/', usuario.Login, name="login"),
    path('registrar/', usuario.Registrar, name="registrar"),
    path('logout/', usuario.Logout, name="logout"),
    path('produto/cadastro', produto.Cadastro, name="cadastro"),
    path('pedido/listar', pedidos.listar_carrinho, name="listar_carrinho"),
    path('pedido/adicionar_ao_carrinho', pedidos.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path('produto/feed_produtos', produto.feed_produtos, name="feed")
]