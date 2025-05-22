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

        self.produto = Produto.objects.create(
            nome='Produto Teste',
            descricao='Descrição',
            preco=Decimal('50.00'),
            vendedor=self.vendedor
        )

        self.client = Client()

    def test_criacao_pedido(self):
        self.client.login(username='cliente', password='senha123')

        response = self.client.post(reverse('criar_pedido'), {
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