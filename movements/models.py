from django.db import models

from accounts.models import CustomUser
from stock.models import Ingredient, Product


class Outflow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(default="outflow")
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Saida por {self.user} {self.product}: {self.amount}"


class Inflow(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through="InflowIngredient")
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(default="inflow")
    date = models.DateTimeField(auto_now_add=True)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Entrada {self.id} por {self.user}"


class InflowIngredient(models.Model):
    inflow = models.ForeignKey("Inflow", on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.inflow} - {self.ingredient}: {self.quantity}"
