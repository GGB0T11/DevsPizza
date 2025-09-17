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
