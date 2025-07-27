from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    qte = models.PositiveIntegerField(default=0)
    min_qte = models.PositiveIntegerField(default=0)
    measure = models.CharField(max_length=10, choices=([("g", "Gramas"), ("kg", "Quilo"), ("unit", "Unidade")]))

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ingredients = models.ManyToManyField(
        Ingredient, through="ProductIngredient", through_fields=("product", "ingredient")
    )
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} - {self.ingredient}: {self.quantity}"
