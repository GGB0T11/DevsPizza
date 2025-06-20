from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    cargo = models.CharField(
        max_length=20,
        choices=[
            ("funcionario", "Funcionario"),
            ("administrador", "Administrador")
        ],
        blank=False
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)
