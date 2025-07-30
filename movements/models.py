from django.db import models


class Movement(models.Model):
    user = models.CharField(max_length=100)
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=([("in", "Entrada"), ("out", "Saida")]))
    date = models.DateTimeField(auto_now_add=True)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.user}: {self.value}"


class MovementInflow(models.Model):
    # related_name para fazer acesso reverso e pegar essas informações
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    measure = models.CharField(max_length=10, choices=([("g", "Gramas"), ("kg", "Quilo"), ("unit", "Unidade")]))

    def __str__(self):
        return f"{self.name}: {self.quantity} - {self.price}"


class MovementOutflow(models.Model):
    # Acesso reverso aqui tambem
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.quantity} - {self.price}"
