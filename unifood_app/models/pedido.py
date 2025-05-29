from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído')
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_cliente')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_vendedor')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    endereco_entrega = models.CharField(max_length=255)
