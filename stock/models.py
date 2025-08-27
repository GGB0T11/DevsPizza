from django.db import models


class Category(models.Model):
    """
    Representa uma categoria de ingredientes.

    Attributes:
        name (str): Nome da categoria.
        description (str): Descrição opcional da categoria.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Representa um ingrediente utilizado nos produtos.

    Attributes:
        name (str): Nome do ingrediente.
        category (Category): Categoria à qual o ingrediente pertence.
        qte (int): Quantidade atual disponível em estoque.
        min_qte (int): Quantidade mínima de segurança no estoque.
        measure (str): Unidade de medida do ingrediente (g/kg/unit).
    """

    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    qte = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    min_qte = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    measure = models.CharField(max_length=10, choices=([("g", "Gramas"), ("kg", "Quilos"), ("unit", "Unidades")]))

    def __str__(self):
        return self.name


class Product(models.Model):
    """Representa um produto disponível para venda.

    Attributes:
        name (str): Nome do produto.
        ingredients (QuerySet[Ingredient]): Ingredientes necessários, relacionados através da tabela ProductIngredient.
        price (Decimal): Preço do produto.
    """

    name = models.CharField(max_length=100, unique=True)
    ingredients = models.ManyToManyField(
        Ingredient, through="ProductIngredient", through_fields=("product", "ingredient")
    )
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# Tabela intermediária para gerenciar o ingrediente e quantidade de cada produto
class ProductIngredient(models.Model):
    """Representa a relação entre produtos e ingredientes.

    Define a quantidade de cada ingrediente utilizada
    na composição de um produto.

    Attributes:
        product (Product): Produto associado.
        ingredient (Ingredient): Ingrediente associado.
        quantity (Decimal): Quantidade do ingrediente necessária para o produto.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        unique_together = ("product", "ingredient")

    def __str__(self):
        return f"{self.product} - {self.ingredient}: {self.quantity}"
