from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    CARGOS = [("func", "Funcionário"),("adm", "Administrador")]
    cargo = models.CharField(max_length=4, choices=CARGOS, default="func")

    def __str__(self):
        return f"{self.username} - {self.get_cargo_display()}"

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Insumo(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    qteAtual = models.PositiveIntegerField(default=0)
    unidadeMedida = models.CharField(max_length=10)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    insumos = models.ManyToManyField(Insumo)

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    TIPOS = [("entrada", "Entrada"), ("saida", "Saida")]
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=TIPOS)
    quantidade = models.PositiveIntegerField(default=1)
    data = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(null=True)

    def __str__(self):
        return f"{self.produto}, {self.quantidade} - {self.get_tipo_disply()}"