from django.urls import path
from .views import usuario, pedidos, produto

urlpatterns = [
    path('login/', usuario.Login, name="login"),
    path('registrar/', usuario.Registrar, name="registrar"),
    path('logout/', usuario.Logout, name="logout"),
    path('produto/cadastro', produto.Cadastro, name="cadastro"),
    path('pedido/listar', pedidos.listar_carrinho, name="listar_carrinho"),
    path('pedido/criar_pedido', pedidos.criar_pedido, name="criar_pedido"),
    path('produto/feed_produtos', produto.feed_produtos, name="feed")
]