from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import transaction

from stock.models import Ingredient, Product

from .models import Movement, MovementInflow, MovementOutflow


def convert_measures(qte: Decimal, origin: str, destiny: str) -> Decimal:
    """Converte Gramas em Kg e vice versa.

    Args:
        qte (Decimal): Quantidade a ser convertida.
        origin (str): Unidade de medida inserida na transação.
        destiny (str): Unidade de medida do item.

    Returns:
        Decimal: Número convertido.
    """

    factors = {
        ("g", "kg"): lambda x: x / 1000,
        ("kg", "g"): lambda x: x * 1000,
        ("g", "g"): lambda x: x,
        ("kg", "kg"): lambda x: x,
        ("unit", "unit"): lambda x: x,
    }
    return factors[(origin, destiny)](qte)


def parse_value_br(value: str, name: str) -> tuple[Decimal | None, list[str]]:
    """Converte valor no formato brasileiro (1.234,56) para Decimal no padrão internacional (1234.56).

    Args:
        value(str): Valor a ser convertido.
        name(str): Nome do item (para retornar caso de erro).

    Returns:
        Decimal, []: Caso a formatação tenha sido concluida ou o número for maior que 9.
        None, errors: Caso a formatação não tenha funcionado ou o número seja menor ou igual a 0.
    """

    errors = []
    try:
        value = value.replace(".", "").replace(",", ".")
        value = Decimal(value)
    except (InvalidOperation, AttributeError):
        errors.append(f"Insira um valor válido para {name}")
        return None, errors

    if value <= 0:
        errors.append(f"Insira um valor maior que 0 para {name}")
        return None, errors
    return value, []


@transaction.atomic
def create_inflow(data: dict, username: str) -> None:
    """Valida e cria uma movimentação de entrada de ingredientes.

    Args:
        data(dict): Requisição contendo as informações a serem preocessadas.
        username(str): Nome do usuário.

    Returns:
        raise: Lista de erros (se houver).
        None: Se a movimentação for registrada.
    """

    errors = []
    ingredients_to_add = []
    value = Decimal("0")

    ingredients_ids = data.getlist("ingredients")
    if not ingredients_ids:
        raise ValidationError(["Selecione ao menos 1 ingrediente"])

    for ingredient_id in ingredients_ids:
        ingredient = Ingredient.objects.get(pk=ingredient_id)

        qte_to_add, qte_errors = parse_value_br(data[f"qi-{ingredient_id}"], ingredient.name)

        price, price_errors = parse_value_br(data[f"pi-{ingredient_id}"], ingredient.name)

        if qte_errors or price_errors:
            errors.extend(qte_errors + price_errors)
            continue

        measure = data[f"m-{ingredient_id}"]
        ingredient.qte += convert_measures(qte_to_add, measure, ingredient.measure)

        ingredients_to_add.append((ingredient, qte_to_add, price, measure))
        value += price

    if errors:
        raise ValidationError(errors)

    Ingredient.objects.bulk_update([i[0] for i in ingredients_to_add], ["qte"])

    movement = Movement.objects.create(
        user=username,
        value=value,
        type="in",
        commentary=data["commentary"],
    )

    for ingredient, qte_added, price, measure in ingredients_to_add:
        MovementInflow.objects.create(
            movement=movement,
            name=ingredient.name,
            quantity=qte_added,
            price=price,
            measure=measure,
        )


@transaction.atomic
def create_outflow(data: dict, username: str) -> None:
    """Valida e cria uma movimentação de saida de produtos.

    Args:
        data(dict): Requisição contendo as informações a serem preocessadas.
        username(str): Nome do usuário.

    Returns:
        raise: Lista de erros (se houver).
        None: Se a movimentação for registrada.
    """

    errors = []
    products_sold = []
    total_value = Decimal("0")

    products_ids = data.getlist("products")
    if not products_ids:
        raise ValidationError(["Selecione ao menos 1 produto"])

    for product_id in products_ids:
        product = Product.objects.get(pk=product_id)
        ingredients_to_reduce = []
        product_errors = []

        quantity, qte_error = parse_value_br(data[f"qp-{product_id}"], product.name)

        if qte_error:
            product_errors.extend(qte_error)
            continue

        if quantity:
            for recipe_item in product.productingredient_set.all():
                ingredient = recipe_item.ingredient
                decrease_qte = recipe_item.quantity * quantity
                remaining = ingredient.qte - decrease_qte

                if remaining < 0:
                    product_errors.append(f"Estoque insuficiente para o ingrediente {ingredient.name}!")
                else:
                    ingredient.qte = remaining
                    ingredients_to_reduce.append(ingredient)

        if product_errors:
            errors.extend(product_errors)
            continue

        value = product.price * quantity
        total_value += value

        Ingredient.objects.bulk_update(ingredients_to_reduce, ["qte"])
        products_sold.append((product.name, quantity, value))

    if errors:
        raise ValidationError(errors)

    movement = Movement.objects.create(
        user=username,
        value=total_value,
        type="out",
        commentary=data["commentary"],
    )

    for name, quantity, price in products_sold:
        MovementOutflow.objects.create(
            movement=movement,
            name=name,
            quantity=quantity,
            price=price,
        )
