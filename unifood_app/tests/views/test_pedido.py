from django.test import TestCase, Client
from django.contrib.auth.models import User
from unifood_app.models import Pedido, Produto, Item_Pedido
from decimal import Decimal
from django.urls import reverse

class PedidoViewTest(TestCase):
    def setUp(self):
        self.cliente = User.objects.create_user(username='cliente', password='senha123')
        self.vendedor = User.objects.create_user(username='vendedor', password='senha123')
        self.cliente2 = User.objects.create_user(username="cliente2", password="senha123")

        self.produto = Produto.objects.create(
            vendedor=self.vendedor,
            nome='Produto Teste',
            descricao='Descrição',
            preco=Decimal('50.00'),
            estoque = 10,
            foto = 'media/produtos/fotos/6159Mountain-Gaot.jpg'
        )

        self.produto2 = Produto.objects.create(
            vendedor=self.vendedor,
            nome='goated',
            descricao='goating',
            preco=Decimal('50.00'),
            estoque = 10,
            foto = 'media/produtos/fotos/6159Mountain-Gaot.jpg'

        )
        self.pedido = Pedido.objects.create(
            cliente = self.cliente,
            vendedor = self.vendedor,
            endereco_entrega = 'logo ali',
            valor_total=Decimal('0.00')
        )

        self.list_users = [self.cliente, self.cliente2]
        self.list_produtos = [self.produto, self.produto2]

        self.client = Client()

    def test_adicionar_ao_carrinho(self):
        self.client.login(username='cliente2', password='senha123')

        response = self.client.post(reverse('adicionar_ao_carrinho'), {
            'produto_id': self.produto.id,
            'endereco_entrega': 'Rua Teste, 123'
        })

        self.assertEqual(response.status_code, 302)

        pedido = Pedido.objects.filter(cliente=self.cliente2).get()
        self.assertIsNotNone(pedido)
        self.assertEqual(pedido.cliente, self.cliente2)
        self.assertEqual(pedido.vendedor, self.vendedor)
        self.assertEqual(pedido.endereco_entrega, 'Rua Teste, 123')
        self.assertEqual(pedido.status, 'pendente')
        self.client.logout()

        print("\nPedidos: Adicionado ao carrinho com sucesso!")
    
    def test_adicionar_o_mesmo_produto_outra_vez(self):
        self.client.login(username='cliente2', password='senha123')

        for _ in range(0,2):
            self.client.post(reverse('adicionar_ao_carrinho'), {
                'produto_id': self.produto.id,
                'endereco_entrega': 'Rua Teste, 123'
            })
        pedido = Pedido.objects.get(cliente=self.cliente2, status='pendente')

        item_pedido = Item_Pedido.objects.get(produto=self.produto, pedido=pedido)
        self.assertEqual(item_pedido.quantidade, 2)

        print(f'\nPedidos: Item {item_pedido.produto.nome} adicionado duas vezes com sucesso!')
        
    def test_listar_carrinho(self):

        for i, user in enumerate(self.list_users):
            self.client.login(username=user.username, password="senha123")

            self.client.post(reverse('adicionar_ao_carrinho'), {
                'produto_id': self.list_produtos[i].id,
                'endereco_entrega': 'Rua Teste, 123'
            })

            self.client.post(reverse('listar_carrinho'))
            self.client.logout()

        print("\nPedidos: Carrinhos listados com sucesso!")

    def test_confirmar_pagamento(self):
        self.assertEqual(self.pedido.status, 'pendente')
        
        self.client.login(username=self.vendedor, password='senha123')
        response = self.client.post(
            reverse('confirmar_pagamento'),
            {
            'pedido_id': self.pedido.id
            })
        
        self.assertEqual(response.status_code, 302)

        self.pedido.refresh_from_db()
        
        self.assertEqual(self.pedido.status, 'concluido')
        
        self.client.logout()
        print("\nPedidos: Pagamento efetuado com sucesso!")

    def test_listar_pedido(self):
        self.client.login(username=self.vendedor, password='senha123')
        response = self.client.get(reverse(
            'listar_pedidos'
                                           ))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Pedido {self.pedido.id}')
        self.assertContains(response, self.cliente.username)
        self.assertContains(response, self.pedido.valor_total)
        self.client.logout()
        print('\nPedidos: Pedidos listados com sucesso!')


    def test_detalhes_pedido_cliente(self):
        self.client.login(username='cliente', password='senha123')
        response = self.client.get(reverse('detalhe_pedido'), {
            'pedido_id': self.pedido.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Pedido {self.pedido.id}')
        self.assertContains(response, self.cliente.username)
        self.assertContains(response, self.vendedor.username)
        self.assertContains(response, self.pedido.endereco_entrega)
        self.assertContains(response, self.pedido.valor_total)
        self.assertContains(response, f'Aguardando confirmação de pagamento pelo vendedor.')
        self.assertNotContains(response, f'Confirmar Pagamento')
        print(f'\nPedidos: Visualização do pedido pelo cliente certo!')
        

    def test_detalhes_pedido_vendedor(self):
        self.client.login(username='vendedor', password='senha123')
        response = self.client.get(reverse('detalhe_pedido'), {
            'pedido_id': self.pedido.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Pedido {self.pedido.id}')
        self.assertContains(response, self.cliente.username)
        self.assertContains(response, self.vendedor.username)
        self.assertContains(response, self.pedido.endereco_entrega)
        self.assertContains(response, self.pedido.valor_total)
        self.assertNotContains(response, f'Aguardando confirmação de pagamento pelo vendedor.')
        self.assertContains(response, f'Confirmar Pagamento')
        print(f'\nPedidos: Visualização do pedido pelo vendedor certo!')
    
    def test_detalhes_pedido_nao_sendo_cliente_nem_vendedor(self):
        self.client.login(username='cliente2', password='senha123')
        response = self.client.get(reverse('detalhe_pedido'), {
            'pedido_id': self.pedido.id
        })
        self.assertEqual(response.status_code, 403)
        print('\nPedidos: Acesso negado para a visuallização dos detalhes do pedido!')
    
    def test_confirmar_pagamento_nao_sendo_vendedor(self):        
        self.client.login(username=self.cliente, password='senha123')
        response = self.client.post(
            reverse('confirmar_pagamento'),
            {
            'pedido_id': self.pedido.id
            })
        
        self.assertEqual(response.status_code, 403)
        print('\nPedidos: Acesso negado para confirmar pagamento não sendo vendedor!')