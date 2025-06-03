from django.urls import path
from .views import usuario, pedidos, produto, item_pedido
from .views.produto import ProdutoCreateAPIView

urlpatterns = [
    path('login/', usuario.Login, name="login"),
    path('registrar/', usuario.Registrar, name="registrar"),
    path('logout/', usuario.Logout, name="logout"),
    path('produto/cadastro', produto.Cadastro, name="cadastro"),
    path('pedido/listar_carrinho', pedidos.listar_carrinho, name="listar_carrinho"),
    path('pedido/listar_pedidos', pedidos.listar_pedidos, name='listar_pedidos'),
    path('pedido/adicionar_ao_carrinho', pedidos.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path('pedido/confirmar_pagamento', pedidos.confirmar_pagamento,name='confirmar_pagamento'),
    path('pedido/detalhe_pedido', pedidos.detalhe_pedido, name='detalhe_pedido'),
    path('produto/feed_produtos', produto.feed_produtos, name="feed"),
    path('item_pedido/listar/<int:pedido_id>/', item_pedido.listar_itens_pedido, name="listar_itens_pedido"),
    path('api/produtos/', ProdutoCreateAPIView.as_view(), name='api-produto-create'),
]

