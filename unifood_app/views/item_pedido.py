from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from unifood_app.models import Pedido, Item_Pedido

@login_required
def listar_itens_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id, cliente=request.user)
    itens = Item_Pedido.objects.filter(pedido=pedido)
    return render(
        request,
        'unifood_app/itens_pedido/lista_itens_pedido.html',
        {'pedido': pedido, 'itens': itens}
    )