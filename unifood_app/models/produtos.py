from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Produto(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    estoque = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='produtos/fotos/', blank=True, null=True)

    def clean(self):
        # Verificando se o preço é negativo
        if self.preco < 0:
            raise ValidationError("O preço não pode ser negativo.")

    def __str__(self):
        return self.nome  # Retornando o nome do produto no método __str__
