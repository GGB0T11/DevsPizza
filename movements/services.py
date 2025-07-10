from django.db import transaction

from .models import Movement


@transaction.atomic
def create_outflow(user, product, amount, commentary):
    for recipe_item in product.productingredient_set.all():
        ingredient = recipe_item.ingredient
        decrease_qte = recipe_item.quantity * amount
        qte = ingredient.qte - decrease_qte
        if qte < 0:
            raise ValueError(f"Estoque insuficiente para o ingrediente: {ingredient.name}")

    for recipe_item in product.productingredient_set.all():
        ingredient = recipe_item.ingredient
        decrease_qte = recipe_item.quantity * amount

        ingredient.qte -= decrease_qte
        ingredient.save()

    movement = Movement.objects.create(
        user=user,
        product=product,
        amount=amount,
        transaction_type="outflow",
        commentary=commentary,
    )

    return movement
