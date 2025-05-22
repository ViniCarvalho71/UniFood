# unifood_app/views/pedidos.py
from django.shortcuts import render, get_object_or_404
from unifood_app.models import Pedido

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})

def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    return render(request, 'pedidos/detalhe.html', {'pedido': pedido})
