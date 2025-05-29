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
        self.list_users = [self.cliente, self.cliente2]
        self.list_produtos = [self.produto, self.produto2]

        self.client = Client()

    def test_adicionar_ao_carrinho(self):
        self.client.login(username='cliente', password='senha123')

        response = self.client.post(reverse('adicionar_ao_carrinho'), {
            'produto_id': self.produto.id,
            'endereco_entrega': 'Rua Teste, 123'
        })

        # Verificar se foi redirecionado (status 302)
        self.assertEqual(response.status_code, 302)

        # Verificar se o pedido foi criado corretamente
        pedido = Pedido.objects.first()
        self.assertIsNotNone(pedido)
        self.assertEqual(pedido.cliente, self.cliente)
        self.assertEqual(pedido.vendedor, self.vendedor)
        self.assertEqual(pedido.endereco_entrega, 'Rua Teste, 123')
        self.assertEqual(pedido.status, 'pendente')

        print("Pedido criado com sucesso")


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

