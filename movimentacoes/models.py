from django.db import models
from estoque.models import Produto
from usuarios.models import Usuario

class Movimentacao(models.Model):
    TIPOS = [("entrada", "Entrada"), ("saida", "Saida")]
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    tipo = models.CharField(max_length=7, choices=TIPOS)
    quantidade = models.PositiveIntegerField(default=1)
    data = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.produto}, {self.quantidade} - {self.get_tipo_display()}"