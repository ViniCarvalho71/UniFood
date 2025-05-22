from decimal import Decimal
from django.test import TestCase
from unifood_app.models import Pedido
from django.contrib.auth import get_user_model

User = get_user_model()

class PedidoModelTest(TestCase):
    def setUp(self):
        '''Cria um usuário para os testes'''

        self.cliente = User.objects.create_user(
            username='cliente',
            email='test@email.com',
            password='senha_cliente'
            )
        self.vendedor = User.objects.create_user(
            username='vendedor',
            email='teste@email.com',
            password='senha_vendedor'
            )
        
    def test_criacao_pedido_valido(self):
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            vendedor=self.vendedor,
            endereco_entrega='Rua Teste, 123',
            valor_total=Decimal('100.00')
        )
        self.assertIsNotNone(pedido.id)
        self.assertEqual(pedido.cliente, self.cliente)
        self.assertEqual(pedido.vendedor, self.vendedor)
        self.assertEqual(pedido.status, 'pendente')
        self.assertEqual(pedido.valor_total, Decimal('100.00'))

        print('Pedido criado com sucesso!')
    
    def test_str_do_pedido(self):
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            vendedor=self.vendedor,
            endereco_entrega='Rua Teste, 123',
            valor_total=Decimal('100.00')
        )
        esperado = f"Pedido {pedido.id} - {self.cliente.username} para {self.vendedor.username}"
        self.assertEqual(str(pedido), esperado)