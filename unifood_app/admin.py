from django.contrib import admin

from .models import usuario, pedido, produtos, item_pedido

admin.site.register(usuario.Usuario)
admin.site.register(pedido.Pedido)
admin.site.register(produtos.Produto)
admin.site.register(item_pedido.Item_Pedido)