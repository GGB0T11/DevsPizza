from django.db import models

from accounts.models import CustomUser


class Inflow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(default="inflow")
    date = models.DateTimeField(auto_now_add=True)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.user}"


class InflowIngredient(models.Model):
    inflow = models.ForeignKey(Inflow, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    measure_unit = models.CharField(max_length=10, default="N/A")

    def __str__(self):
        return f"{self.name}: {self.quantity}"


class Outflow(models.Model):
    product = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(default="outflow")
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Saida por {self.user} {self.product}: {self.amount}"
