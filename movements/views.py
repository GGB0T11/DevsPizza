from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from core.decorators import admin_required
from stock.models import Ingredient, Product

from .models import Movement, MovementInflow, MovementOutflow


@login_required
@require_http_methods(["GET", "POST"])
def movement_create(request):
    if request.method == "GET":
        context = {
            "products": Product.objects.all(),
            "ingredients": Ingredient.objects.all(),
            "measures": MovementInflow._meta.get_field("measure").choices,
        }
        return render(request, "movement_create.html", context)

    else:
        user = request.user
        transaction_type = request.POST.get("transaction_type")
        commentary = request.POST.get("commentary")

        if transaction_type == "inflow":
            ingredients_ids = request.POST.getlist("ingredients")
            ingredients_to_add = []
            value = 0

            for ingredient_id in ingredients_ids:
                ingredient = Ingredient.objects.get(pk=ingredient_id)
                try:
                    qte_to_add = Decimal(request.POST.get(f"q-{ingredient_id}"))
                    price = Decimal(request.POST.get(f"p-{ingredient_id}"))  # NOTE: tenho que fazer um outro try...
                except ValueError:
                    messages.error(request, f"Insira uma quantidade válida para o ingrediente {ingredient.name}!")
                    return redirect("movement_list")

                measure = request.POST.get(f"m-{ingredient_id}")
                if measure == "kg":
                    multiplier = 1000
                else:
                    multiplier = 1

                ingredient.qte += qte_to_add * multiplier
                ingredients_to_add.append((ingredient, qte_to_add, price, measure))

                value += qte_to_add * price

            Ingredient.objects.bulk_update([i[0] for i in ingredients_to_add], ["qte"])

            movement = Movement.objects.create(
                user=user,
                value=value,
                type="in",
                commentary=commentary,
            )

            for ingredient, qte_added, price, measure in ingredients_to_add:
                MovementInflow.objects.create(
                    movement=movement,
                    name=ingredient.name,
                    quantity=qte_added,
                    price=price,
                    measure=measure,
                )

        elif transaction_type == "outflow":
            products_ids = request.POST.getlist("products")
            products_sold = []
            total_value = 0

            for product_id in products_ids:
                product = Product.objects.get(pk=product_id)
                ingredients_to_reduce = []

                try:
                    quantity = int(request.POST.get(f"q-{product_id}"))
                except ValueError:
                    messages.error(request, f"Insira uma quantidade válida para o produto {product.name}")
                    return redirect("movement_list")

                for recipe_item in product.productingredient_set.all():
                    ingredient = recipe_item.ingredient
                    decrease_qte = recipe_item.quantity * quantity
                    remaining = ingredient.qte - decrease_qte

                    if remaining < 0:
                        messages.error(request, f"Estoque insuficiente para o ingrediente {ingredient.name}!")
                        return redirect("movement_list")

                    ingredient.qte = remaining
                    ingredients_to_reduce.append(ingredient)

                value = product.price * quantity
                total_value += value

                Ingredient.objects.bulk_update(ingredients_to_reduce, ["qte"])

                products_sold.append((product.name, quantity, value))

            movement = Movement.objects.create(
                user=user,
                value=total_value,
                type="out",
                commentary=commentary,
            )

            for name, quantity, price in products_sold:
                MovementOutflow.objects.create(
                    movement=movement,
                    name=name,
                    quantity=quantity,
                    price=price,
                )

        else:
            messages.error(request, "Tipo de movimentação inválida!")
            return redirect("movement_list")

        messages.success(request, "Movimentação registrada com sucesso!")
        return redirect("movement_list")


@login_required
@require_http_methods(["GET"])
def movement_list(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        start_dt = timezone.make_aware(start_dt)
        end_dt = timezone.make_aware(end_dt)

        movements = Movement.objects.filter(date__range=(start_dt, end_dt)).order_by("-date")
    else:
        movements = Movement.objects.all().order_by("-date")

    context = {"movements": movements}
    return render(request, "movement_list.html", context)


@login_required
@require_http_methods(["GET"])
def movement_detail(request, id):
    movement = get_object_or_404(Movement, id=id)

    context = {"movement": movement}
    return render(request, "movement_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def movement_delete(request, id):
    movement = get_object_or_404(Movement, id=id)

    if request.method == "GET":
        context = {"movement": movement}
        return render(request, "movement_delete.html", context)

    else:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            messages.error(request, "A senha que você inseriu está incorreta!")
            return redirect("movement_list")

        movement.delete()

        messages.success(request, "Movimentação deletada com sucesso!")
        return redirect("movement_list")
