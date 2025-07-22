from django.contrib import messages
from django.db import transaction

from stock.models import Ingredient, Product

from .models import Inflow, InflowIngredient, Outflow


@transaction.atomic
def create_inflow(request, user, ingredients_ids, commentary, post_data):
    ingredients_to_add = []

    for ingredient_id in ingredients_ids:
        try:
            add_qte = float(post_data.get(f"q-{ingredient_id}"))
        except ValueError:
            ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
            messages.error(request, f"Forneça uma quantidade válida para o ingrediente {ingredient_name}!")
            return False

        if add_qte < 0:
            ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
            messages.error(request, f"forneça uma quantidade maior que 0 para o ingrediente {ingredient_name}!")
            return False

        ingredient = Ingredient.objects.get(pk=ingredient_id)
        ingredient.qte += add_qte
        ingredients_to_add.append((ingredient, add_qte))

    Ingredient.objects.bulk_update([i[0] for i in ingredients_to_add], ["qte"])

    movement = Inflow.objects.create(
        user=user,
        commentary=commentary,
    )

    for ingredient, quantity_added in ingredients_to_add:
        print(f"Salvando: {ingredient.name} - {quantity_added}")
        InflowIngredient.objects.create(
            inflow=movement,
            ingredient=ingredient,
            quantity=quantity_added,
        )

    return movement


@transaction.atomic
def create_outflow(request, user, product, amount, commentary):
    product = Product.objects.get(pk=product)
    ingredients_to_reduce = []

    for recipe_item in product.productingredient_set.all():
        ingredient = recipe_item.ingredient
        decrease_qte = recipe_item.quantity * int(amount)
        remaining = ingredient.qte - decrease_qte
        if remaining < 0:
            messages.error(request, f"Estoque insuficiente para o ingrediente: {ingredient.name}")
            return False

        ingredient.qte = remaining
        ingredients_to_reduce.append(ingredient)

    Ingredient.objects.bulk_update(ingredients_to_reduce, ["qte"])

    movement = Outflow.objects.create(
        user=user,
        product=product,
        amount=amount,
        transaction_type="outflow",
        commentary=commentary,
    )

    return movement
