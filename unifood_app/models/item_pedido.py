from django.db import models
from django.core.validators import MinValueValidator
from unifood_app.models import Pedido, Produto

class Item_Pedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def subtotal(self):
        return self.quantidade * self.preco_unitario
