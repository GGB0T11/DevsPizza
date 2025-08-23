from django.db import models


class Movement(models.Model):
    """Representa uma movimentação.

    Atributes:
        user (str): Nome do responsável pela movimentação.
        value (Decimal): Valor total da movimentação.
        type (str): Tipo de movimentação (in/out).
        date (timestamp): Data da movimentação.
        commentary (str): Comentário sobre a transação movimentação.

    """

    user = models.CharField(max_length=100)
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=([("in", "Entrada"), ("out", "Saida")]))
    date = models.DateTimeField(auto_now_add=True)
    commentary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.user}: {self.value}"


class MovementInflow(models.Model):
    """Representa uma movimentação de entrada (ingredientes).

    Atributes:
        movement (Fk): Chave estrangeira para a movimentação base com o nome de ingredients.
        name (str): Nome do ingrediente.
        quantity (Decimal): Quantidade adicionada.
        price (Decimal): Preço pago.
        measure (str) Unidade de Medida (g/kg/unit).

    """

    # related_name para fazer acesso reverso e pegar essas informações
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    measure = models.CharField(max_length=10, choices=([("g", "Gramas"), ("kg", "Quilo"), ("unit", "Unidade")]))

    def __str__(self):
        return f"{self.name}: {self.quantity} - {self.price}"


class MovementOutflow(models.Model):
    """Representa uma movimentação de saida (produtos).

    Atributes:
        movement (Fk): Chave estrangeira para a movimentação base com o nome de products.
        name (str): Nome do produto.
        quantity (int): Quantidade vendida.
        price (Decimal): Preço.

    """

    # Acesso reverso aqui tambem
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.quantity} - {self.price}"
