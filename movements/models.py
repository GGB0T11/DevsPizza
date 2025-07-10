from django.db import models

from accounts.models import CustomUser
from stock.models import Product


class Movement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(
        max_length=7,
        choices=[("inflow", "Inflow"), ("outflow", "Outflow")],
        blank=False,
    )
    amount = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product}, {self.amount} {self.get_type_display()}"
