from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model




class Usuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    ra = models.CharField(max_length=10, unique=True)
    eh_vendedor = models.IntegerField(default=0) # 0 = Cliente, 1 = Vendedor
