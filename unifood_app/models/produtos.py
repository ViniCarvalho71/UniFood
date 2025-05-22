from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Modelos Produto, Pedido e Item_Pedido (sem alterações)
class Produto(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    estoque = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='produtos/fotos/', blank=True, null=True)

    def _str_(self):
        return self.nome
