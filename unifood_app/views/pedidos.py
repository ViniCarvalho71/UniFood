# views.py
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from unifood_app.models import Pedido, Produto, Item_Pedido
from decimal import Decimal

@login_required
def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        endereco = request.POST.get('endereco_entrega')

        produto = get_object_or_404(Produto, id=produto_id)

        pedido, pedido_criado = Pedido.objects.get_or_create(
            cliente=request.user,
            vendedor= produto.vendedor,
            endereco_entrega=endereco,
            valor_total=Decimal('0.00') 
        )

        item_pedido, item_criado = Item_Pedido.objects.get_or_create(
            pedido=pedido,
            produto=produto,
            defaults={
            'quantidade': 1,
            'preco_unitario': produto.preco
            }
        )

        if not item_criado:
            item_pedido.quantidade += 1
            item_pedido.save()

        itens = Item_Pedido.objects.filter(pedido=pedido)
        total = sum([i.subtotal() for i in itens])
        pedido.valor_total = total
        pedido.save()

        return redirect('pedidos/listar_carrinho')

    return redirect('templates/unifood_app/usuario/base_page') 

def listar_carrinho(request):
    carrinho = Pedido.objects.filter(
        cliente=request.user
        )
    return render(
        request,
        'unifood_app/pedidos/pagina_do_carrinho.html',
        {'carrinho': carrinho}
        )


def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    return render(request, 'pedidos/detalhe.html', {'pedido': pedido})