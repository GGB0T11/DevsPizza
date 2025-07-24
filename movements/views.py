from datetime import datetime
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from stock.models import Ingredient, Product

from .models import Inflow, InflowIngredient, Outflow


@login_required
@require_http_methods(["GET", "POST"])
def movement_create(request):
    if request.method == "GET":
        context = {"products": Product.objects.all(), "ingredients": Ingredient.objects.all()}
        return render(request, "movement_create.html", context)

    else:
        user = request.user
        transaction_type = request.POST.get("transaction_type")
        commentary = request.POST.get("commentary")

        if transaction_type == "inflow":
            ingredients_ids = request.POST.getlist("ingredients")
            ingredients_to_add = []

            for ingredient_id in ingredients_ids:
                try:
                    add_qte = float(request.POST.get(f"q-{ingredient_id}"))
                except ValueError:
                    ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
                    messages.error(request, f"Insira uma quantodade válida para o ingrediente {ingredient_name}!")
                    return redirect("movement_list")

                ingredient = Ingredient.objects.get(pk=ingredient_id)
                ingredient.qte += add_qte
                ingredients_to_add.append((ingredient, add_qte))

            Ingredient.objects.bulk_update([i[0] for i in ingredients_to_add], ["qte"])

            movement = Inflow.objects.create(
                user=user,
                commentary=commentary,
            )

            for ingredient, qte_added in ingredients_to_add:
                InflowIngredient.objects.create(
                    inflow=movement,
                    ingredient=ingredient,
                    quantity=qte_added,
                )

            messages.success(request, "Movimentação registrada com sucesso!")
            return redirect("movement_list")

        elif transaction_type == "outflow":
            product_id = request.POST.get("product_id")
            amount = request.POST.get("amount")

            product = Product.objects.get(pk=product_id)
            ingredients_to_reduce = []

            for recipe_item in product.productingredient_set.all():
                ingredient = recipe_item.ingredient
                decrease_qte = recipe_item.quantity * int(amount)
                remaining = ingredient.qte - decrease_qte

                if remaining < 0:
                    messages.error(request, f"Estoque insuficiente para o ingrediente {ingredient.name}!")
                    return redirect("movement_list")

                ingredient.qte = remaining
                ingredients_to_reduce.append(ingredient)

            Ingredient.objects.bulk_update(ingredients_to_reduce, ["qte"])

            Outflow.objects.create(
                user=user,
                product=product,
                amount=amount,
                commentary=commentary,
            )

            messages.success(request, "Movimentação registrada com sucesso!")
            return redirect("movement_list")

        else:
            messages.error(request, "Tipo de movimentação inválida!")
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

        inflow = Inflow.objects.filter(date__range=(start_dt, end_dt))
        outflow = Outflow.objects.filter(date__range=(start_dt, end_dt))
    else:
        inflow = Inflow.objects.all()
        outflow = Outflow.objects.all()

    combined = list(chain(inflow, outflow))
    sorted_combined = sorted(combined, key=lambda x: x.date, reverse=True)

    context = {"movements": sorted_combined}
    return render(request, "movement_list.html", context)


@login_required
@require_http_methods(["GET"])
def movement_detail(request, transaction_type, id):
    if transaction_type == "inflow":
        movement = get_object_or_404(Inflow, id=id)
        context = {
            "movement": movement,
            "ingredients": movement.inflowingredient_set.all() if isinstance(movement, Inflow) else None,
        }
    elif transaction_type == "outflow":
        movement = get_object_or_404(Outflow, id=id)
        context = {"movement": movement}
    else:
        messages.error(request, "Tipo de movimentação inválido!")
        return redirect("movement_list")

    print(movement.date)
    return render(request, "movement_detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def movement_delete(request, transaction_type, id):
    if transaction_type == "inflow":
        movement = get_object_or_404(Inflow, id=id)
    elif transaction_type == "outflow":
        movement = get_object_or_404(Outflow, id=id)
    else:
        messages.error(request, "Tipo de movimentação inválido!")
        return redirect("movement_list")

    if request.method == "GET":
        context = {"movement": movement}
        return render(request, "movement_delete.html", context)

    else:
        movement.delete()

        messages.success(request, "Movimentação deletada com sucesso!")
        return redirect("movement_list")
