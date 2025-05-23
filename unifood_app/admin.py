from django.contrib import admin

from .models import usuario, pedido, produtos

admin.site.register(usuario.Usuario)
admin.site.register(pedido.Pedido)
admin.site.register(produtos.Produto)
