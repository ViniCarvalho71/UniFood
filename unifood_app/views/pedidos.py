# views.py
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from unifood_app.models import Pedido
from unifood_app.models import Produto  # Ainda não foi criado o de produto
from decimal import Decimal

@login_required
def criar_pedido(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        endereco = request.POST.get('endereco_entrega')

        produto = get_object_or_404(Produto, id=produto_id)

        pedido = Pedido.objects.create(
            cliente=request.user,
            vendedor= produto.vendedor,
            endereco_entrega=endereco,
            valor_total=Decimal('0.00') 
        )

        return redirect('pagina_do_carrinho')  # Substituir pelo seu nome de url

    return redirect('pagina_de_produtos')  # Se não for POST, volta para produtos

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})

def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    return render(request, 'pedidos/detalhe.html', {'pedido': pedido})