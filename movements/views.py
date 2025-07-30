from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware
from django.views.decorators.http import require_http_methods
from fpdf import FPDF

from core.decorators import admin_required
from stock.models import Ingredient, Product

from .models import Movement, MovementInflow, MovementOutflow


def convert_measures(qte, origin, destiny):
    factors = {
        ("g", "kg"): lambda x: x / 1000,
        ("kg", "g"): lambda x: x * 1000,
        ("g", "g"): lambda x: x,
        ("kg", "kg"): lambda x: x,
        ("unit", "unit"): lambda x: x,
    }
    try:
        return factors[(origin, destiny)](qte)
    except KeyError:
        raise ValueError(f"Conversão inválida de {origin} para {destiny}")


@login_required
@require_http_methods(["GET", "POST"])
def movement_create(request):
    context = {
        "products": Product.objects.all(),
        "ingredients": Ingredient.objects.all(),
        "type_choices": Movement._meta.get_field("type").choices,
    }

    if request.method == "GET":
        return render(request, "movement_create.html", context)

    else:
        try:
            user = request.user
            transaction_type = request.POST.get("type")
            commentary = request.POST.get("commentary")

            if transaction_type == "in":
                ingredients_ids = request.POST.getlist("ingredients")
                ingredients_to_add = []
                value = 0

                for ingredient_id in ingredients_ids:
                    ingredient = Ingredient.objects.get(pk=ingredient_id)
                    try:
                        qte_to_add = Decimal(request.POST.get(f"qi-{ingredient_id}"))
                        price = Decimal(request.POST.get(f"pi-{ingredient_id}"))
                    except (InvalidOperation, ValueError):
                        raise Exception(f"Insira um valor válido para o ingrediente {ingredient.name}!")

                    measure = request.POST.get(f"m-{ingredient_id}")

                    try:
                        converted_qte = convert_measures(qte_to_add, measure, ingredient.measure)
                        ingredient.qte += converted_qte
                    except ValueError:
                        raise Exception(f"Insira uma unidade de medida válida para o ingrediente {ingredient.name}")

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

            elif transaction_type == "out":
                products_ids = request.POST.getlist("products")
                products_sold = []
                total_value = 0

                for product_id in products_ids:
                    product = Product.objects.get(pk=product_id)
                    ingredients_to_reduce = []

                    try:
                        quantity = int(request.POST.get(f"qp-{product_id}"))
                    except ValueError:
                        raise Exception(f"Insira uma quantidade válida para o produto {product.name}")

                    for recipe_item in product.productingredient_set.all():
                        ingredient = recipe_item.ingredient
                        decrease_qte = recipe_item.quantity * quantity
                        remaining = ingredient.qte - decrease_qte

                        if remaining < 0:
                            raise Exception(f"Estoque insuficiente para o ingrediente {ingredient.name}!")

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
                raise Exception("Tipo de movimentação inválida!")

        except Exception as e:
            messages.error(request, str(e))
            return render(request, "movement_create.html", context)

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
    context = {"movement": movement}

    if request.method == "GET":
        return render(request, "movement_delete.html", context)

    else:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            messages.error(request, "A senha que você inseriu está incorreta!")
            return render(request, "movement_delete.html", context)

        movement.delete()

        messages.success(request, "Movimentação deletada com sucesso!")
        return redirect("movement_list")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def report(request):
    if request.method == "GET":
        return render(request, "report.html")

    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    if not (start_date and end_date):
        messages.error(request, "Insira uma data válida!")
        return render(request, "report.html", {"error": True})

    start_dt = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
    end_dt = make_aware(datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S"))

    movements = Movement.objects.filter(date__range=(start_dt, end_dt)) \
        .select_related("user") \
        .prefetch_related("ingredients", "products") \
        .order_by("-date")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Relatório de Movimentações", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, f"Período: {start_date} até {end_date}", ln=True, align="C")
    pdf.ln(5)

    for movement in movements:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{movement.get_type_display()} - {movement.date.strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 8, f"Responsável: {movement.user.get_full_name()}", ln=True)
        pdf.cell(0, 8, f"Valor total: R$ {movement.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True)

        pdf.ln(2)
        if movement.type == "in":
            pdf.set_font("Arial", "B", 10)
            pdf.cell(60, 8, "Nome", border=1)
            pdf.cell(40, 8, "Quantidade", border=1)
            pdf.cell(30, 8, "Medida", border=1)
            pdf.cell(40, 8, "Preço (R$)", border=1)
            pdf.ln()

            for ing in movement.ingredients.all():
                pdf.set_font("Arial", size=10)
                pdf.cell(60, 8, ing.name, border=1)
                pdf.cell(40, 8, f"{ing.quantity}", border=1)
                pdf.cell(30, 8, ing.get_measure_display(), border=1)
                pdf.cell(40, 8, f"{ing.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), border=1)
                pdf.ln()
        else:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(60, 8, "Nome", border=1)
            pdf.cell(40, 8, "Quantidade", border=1)
            pdf.cell(40, 8, "Preço (R$)", border=1)
            pdf.ln()

            for prod in movement.products.all():
                pdf.set_font("Arial", size=10)
                pdf.cell(60, 8, prod.name, border=1)
                pdf.cell(40, 8, f"{prod.quantity}", border=1)
                pdf.cell(40, 8, f"{prod.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), border=1)
                pdf.ln()

        pdf.ln(5)  # espaço entre movimentos

    response = HttpResponse(pdf.output(dest="S").encode("latin1"), content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename='relatorio.pdf'"
    return response
