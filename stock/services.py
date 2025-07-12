from django.core.exceptions import ValidationError

from .models import Ingredient, Product, ProductIngredient


def register_product(product_name, selected_ids, post_data):
    ingredients_to_create = []

    for ingredient_id in selected_ids:
        quantity = float(post_data.get(f"q-{ingredient_id}"))

        if quantity > 0:
            ingredients_to_create.append({"ingredient_id": int(ingredient_id), "quantity": quantity})
        else:
            ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
            raise ValidationError(f"Forneça uma quantidade válida para o ingrediente: {ingredient_name}")

    product = Product.objects.create(name=product_name)

    for data in ingredients_to_create:
        ProductIngredient.objects.create(
            product=product,
            ingredient_id=data["ingredient_id"],
            quantity=data["quantity"],
        )

    return product


def update_product(product_instance, new_name, selected_ids, post_data):
    product_instance.name = new_name
    product_instance.save(update_fields=["name"])

    old_ingredients_ids = set(product_instance.productingredient_set.values_list("ingredient_id", flat=True))
    new_ingredients_ids = set(int(pk) for pk in selected_ids)

    ids_to_remove = old_ingredients_ids - new_ingredients_ids
    if ids_to_remove:
        ProductIngredient.objects.filter(product=product_instance, ingredient_id__in=ids_to_remove).delete()

    for ingredient_id in new_ingredients_ids:
        quantity = float(post_data.get(f"q-{ingredient_id}"))

        if quantity <= 0:
            ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
            raise ValidationError(f"Forneça uma quantidade válida para o ingrediente: {ingredient_name}")

        ProductIngredient.objects.update_or_create(
            product=product_instance,
            ingredient_id=ingredient_id,
            defaults={"quantity": quantity},
        )

    return product_instance
