from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Insumo(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    qte_atual = models.PositiveIntegerField(default=0)
    unidade_medida = models.CharField(max_length=10)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    insumos = models.ManyToManyField(Insumo)

    def __str__(self):
        return self.nome
