from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unifood_app.models import Pedido, Produto, Item_Pedido
from decimal import Decimal

class PedidoViewTest(TestCase):
    def setUp(self):
        # ...existing code...
        self.client = Client()
        self.cliente = User.objects.create_user(username='cliente', password='senha123')
        self.vendedor = User.objects.create_user(username='vendedor', password='senha123')
        self.produto = Produto.objects.create(
            vendedor=self.vendedor,
            nome='Produto Teste',
            descricao='Descrição do produto teste',
            preco=Decimal('50.00'),
            estoque=10,
            foto='produtos/fotos/produto_teste.jpg'
        )
        

    # ...existing tests...

    def test_listar_itens_pedido(self):
        # Cria pedido e item
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            vendedor=self.vendedor,
            valor_total=Decimal('100.00'),
            endereco_entrega='Rua Teste, 123'
        )
        item = Item_Pedido.objects.create(
            pedido=pedido,
            produto=self.produto,
            quantidade=2,
            preco_unitario=Decimal('50.00')
        )

        self.client.login(username='cliente', password='senha123')
        url = reverse('listar_itens_pedido', args=[pedido.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Produto Teste')
        self.assertContains(response, '2')
        self.assertContains(response, '50.00')