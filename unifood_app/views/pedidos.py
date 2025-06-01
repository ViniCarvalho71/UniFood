# views.py
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from unifood_app.models import Pedido, Produto, Item_Pedido
from decimal import Decimal
from django.http import HttpResponse
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
            status='pendente',
            defaults={'valor_total':Decimal('0.00')} 
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

        return redirect('unifood_app/pedidos/lista_pedidos.html')

    return redirect('unifood_app/usuario/base_page.html') 

def listar_carrinho(request):
    carrinho = Pedido.objects.filter(
        cliente=request.user,
        status='pendente'
        )
    return render(
        request,
        'unifood_app/pedidos/pagina_do_carrinho.html',
        {'carrinho': carrinho}
        )

def confirmar_pagamento(request):
    if request.method == 'POST':    
        pedido_id = request.POST.get("pedido_id")
        pedido = get_object_or_404(Pedido, id=pedido_id, status='pendente')
        if request.user != pedido.vendedor:
            return HttpResponse("Você não tem permissão para concluir este pagamento", status=403)
        pedido.status = "concluido"
        pedido.save()
        return redirect(
            'listar_pedidos'
        )

def listar_pedidos(request):
    pedidos = Pedido.objects.filter(vendedor=request.user)

    contexto = {'pedidos':pedidos}
    return render(
        request,
        'unifood_app/pedidos/lista_pedidos.html',
        contexto
        )

def detalhe_pedido(request):
    pedido_id = request.GET.get("pedido_id")
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.cliente != request.user and pedido.vendedor != request.user:
        return HttpResponse('Você não tem permissão para acessar este pedido.', status=403)
    
    return render(request,
                  'unifood_app/pedidos/detalhe_pedido.html',
                  {'pedido': pedido}
                  )