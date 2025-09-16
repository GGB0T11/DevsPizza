from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError

from .models import Ingredient, Product, ProductIngredient


def parse_value_br(value: str, msg: str) -> tuple[Decimal | None, list[str]]:
    """Converte valor no formato brasileiro (1.234,56) para Decimal no padrão internacional (1234.56).

    Args:
        value(str): Valor a ser convertido.
        msg(str): Mensagem (para retornar caso de erro).

    Returns:
        Decimal, []: Caso a formatação tenha sido concluida ou o número for maior que 9.
        None, errors: Caso a formatação não tenha funcionado ou o número seja menor ou igual a 0.
    """

    errors = []
    try:
        value = value.replace(".", "").replace(",", ".")
        value = Decimal(value)
        if value <= 0:
            errors.append(f"{msg}")
    except (InvalidOperation, AttributeError):
        errors.append(f"{msg}")
        return None, errors
    return value, []


def create_food(name: str, price: str, ingredients_ids: list, data: dict) -> None:
    """Cria um produto (Comida)

    Args:
        name(str): Nome do produto.
        price(str): Preço do produto.
        ingredients_ids(List): Id's dos ingredientes do produto.
        data(dict): Requisição contendo as informações a serem preocessadas.

    Returns:
        raise: Lista de erros (se houver).
        None: Se a movimentação for registrada.
    """

    errors = []

    price, price_error = parse_value_br(price, "Insira um preço válido!")

    if price_error:
        errors.append(price_error)

    ingredients_to_create = []

    for ingredient_id in ingredients_ids:
        quantity = data.get(f"q-{ingredient_id}")
        quantity, quantity_error = parse_value_br(
            str(quantity), f"Insira uma quantidade válida para {Ingredient.objects.get(pk=ingredient_id).name}"
        )

        if quantity_error:
            errors.append(quantity_error)
            continue

        ingredients_to_create.append((int(ingredient_id), quantity))

    if errors:
        raise ValidationError(errors)

    product = Product.objects.create(name=name, type="food", price=price)

    for ingredient_id, quantity in ingredients_to_create:
        ProductIngredient.objects.create(
            product=product,
            ingredient_id=ingredient_id,
            quantity=quantity,
        )


def create_drink(name: str, price: str, quantity: int):
    """Cria um produto (Bebida)

    Args:
        name(str): Nome do produto.
        price(str): Preço do produto.
        quantity(int): quantidade de bebida em estoque.

    Returns:
        raise: Lista de erros (se houver).
        None: Se a movimentação for registrada.
    """

    price, price_error = parse_value_br(price, "Insira um preço válido!")

    if price_error:
        raise ValidationError([price_error])

    product = Product.objects.create(name=name, type="drink", quantity=quantity)
