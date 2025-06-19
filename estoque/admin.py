from django.contrib import admin

from .models import Categoria, Insumo, Produto

admin.site.register(Categoria)
admin.site.register(Insumo)
admin.site.register(Produto)