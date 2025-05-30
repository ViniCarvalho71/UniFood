from django.test import TestCase, Client
from django.contrib.auth.models import User
from unifood_app.models import Pedido
from unifood_app.models import Produto
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
        self.client.login(username='cliente', password='senha123')

        response = self.client.post(reverse('adicionar_ao_carrinho'), {
            'produto_id': self.produto.id,
            'endereco_entrega': 'Rua Teste, 123'
        })

        self.assertEqual(response.status_code, 302)

        pedido = Pedido.objects.first()
        self.assertIsNotNone(pedido)
        self.assertEqual(pedido.cliente, self.cliente)
        self.assertEqual(pedido.vendedor, self.vendedor)
        self.assertEqual(pedido.endereco_entrega, 'logo ali')
        self.assertEqual(pedido.status, 'pendente')

        print("Adicionado ao carrinho com sucesso")


    def test_listar_carrinho(self):

        for i, user in enumerate(self.list_users):
            self.client.login(username=user.username, password="senha123")

            self.client.post(reverse('adicionar_ao_carrinho'), {
                'produto_id': self.list_produtos[i].id,
                'endereco_entrega': 'Rua Teste, 123'
            })

            self.client.post(reverse('listar_carrinho'))
            self.client.logout()

        print("Carrinhos listados com sucesso")

    def test_confirmar_pagamento(self):
        self.assertEqual(self.pedido.status, 'pendente')
        
        self.client.login(username=self.vendedor, password='senha123')
        response = self.client.post(reverse('confirmar_pagamento'),{
            'pedido_id': self.pedido.id
        })
        
        self.assertEqual(response.status_code, 302)

        self.pedido.refresh_from_db()
        
        self.assertEqual(self.pedido.status, 'concluido')
        
        self.client.logout()
        print("Pagamento efetuado com sucesso!")