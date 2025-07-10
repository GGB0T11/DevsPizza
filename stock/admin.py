from django.contrib import admin

from .models import Category, Ingredient, Product, ProductIngredient


class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductIngredientInline]


admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Product, ProductAdmin)
