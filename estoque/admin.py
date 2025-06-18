from django.contrib import admin

# Register your models here.
from .models import Usuario, Categoria, Insumo, Produto, Movimentacao

admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Insumo)
admin.site.register(Produto)
admin.site.register(Movimentacao)