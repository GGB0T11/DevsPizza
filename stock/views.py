from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.decorators import admin_required

from .models import Category, Ingredient, Product, ProductIngredient


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def category_create(request):
    if request.method == "GET":
        return render(request, "category_create.html")

    else:
        name = request.POST.get("name")
        description = request.POST.get("description")

        if Category.objects.filter(name__iexact=name):
            messages.error(request, "A categoria que deseja cadastrar já existe!")
            return redirect("category_list")

        category = Category.objects.create(name=name, description=description)

        category.save()

        messages.success(request, "Categoria criada com sucesso!")
        return redirect("category_list")


@login_required
@admin_required
@require_http_methods(["GET"])
def category_list(request):
    context = {"categories": Category.objects.all()}
    return render(request, "category_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def category_detail(request, id):
    context = {"category": get_object_or_404(Category, id=id)}

    return render(request, "category_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    context = {"category": category}

    if request.method == "GET":
        return render(request, "category_update.html", context)

    else:
        name = request.POST.get("name")

        if Category.objects.filter(name__iexact=name).exclude(id=category.id).exists():
            messages.error(request, "O novo nome que deseja inserir já está associado a uma categoria")
            return render(request, "category_update.html", context)

        category.name = name
        category.description = request.POST.get("description")
        category.save()

        messages.success(request, "Categoria alterada com sucesso!")
        return redirect("category_list")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "GET":
        context = {"category": category}
        return render(request, "category_delete.html", context)

    else:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            messages.error(request, "A senha que você inseriu está incorreta!")
            return redirect("category_list")

        category.delete()

        messages.success(request, "Categoria deletada com sucesso!")
        return redirect("category_list")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def ingredient_create(request):
    if request.method == "GET":
        context = {
            "categories": Category.objects.all(),
            "measure_choices": Ingredient._meta.get_field("measure").choices,
        }
        return render(request, "ingredient_create.html", context)

    else:
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        qte = request.POST.get("qte")
        min_qte = request.POST.get("min_qte")
        measure = request.POST.get("measure")

        category = get_object_or_404(Category, id=category_id)

        if Ingredient.objects.filter(name__iexact=name).exists():
            messages.error(request, "O ingrediente que deseja cadastrar já existe!")
            return redirect("ingredient_list")

        ingredient = Ingredient.objects.create(
            name=name,
            category=category,
            qte=qte,
            min_qte=min_qte,
            measure=measure,
        )

        ingredient.save()

        messages.success(request, "Ingrediente cadastrado com sucesso!")
        return redirect("ingredient_list")


@login_required
@admin_required
@require_http_methods(["GET"])
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    categories = Category.objects.all()

    field = request.GET.get("field")
    value = request.GET.get("value")

    if field and value:
        if field == "name":
            ingredients = ingredients.filter(name__icontains=value)
        elif field == "category":
            ingredients = ingredients.filter(category__name__icontains=value)
        elif field == "qte":
            ingredients = ingredients.filter(qte=value)
        elif field == "min_qte":
            ingredients = ingredients.filter(min_qte=value)

    context = {
        "ingredients": ingredients,
        "categories": categories,
        "field": field,
        "value": value,
    }
    return render(request, "ingredient_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def ingredient_detail(request, id):
    context = {"ingredient": get_object_or_404(Ingredient, id=id)}
    return render(request, "ingredient_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def ingredient_update(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    context = {
        "ingredient": ingredient,
        "categories": Category.objects.all(),
        "measure_choices": Ingredient._meta.get_field("measure").choices,
    }
    if request.method == "GET":
        return render(request, "ingredient_update.html", context)

    else:
        name = request.POST.get("name")

        if Ingredient.objects.filter(name__iexact=name).exclude(id=ingredient.id).exists():
            messages.error(request, "O novo nome que deseja inserir já está associado a um ingrediente")
            return redirect("ingredient_list")

        ingredient.name = name
        category_id = request.POST.get("category")
        ingredient.category = get_object_or_404(Category, id=category_id)
        ingredient.qte = request.POST.get("qte")
        ingredient.min_qte = request.POST.get("min_qte")
        ingredient.measure = request.POST.get("measure")

        ingredient.save()

        messages.success(request, "Ingrediente alterado com sucesso!")
        return redirect("ingredient_list")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def ingredient_delete(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)

    if request.method == "GET":
        context = {"ingredient": ingredient}
        return render(request, "ingredient_delete.html", context)

    else:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            messages.error(request, "A senha que você inseriu está incorreta!")
            return redirect("ingredient_list")

        ingredient.delete()

        messages.success(request, "Ingrediente deletado com sucesso!")
        return redirect("ingredient_list")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def product_create(request):
    if request.method == "GET":
        context = {"ingredients": Ingredient.objects.all()}
        return render(request, "product_create.html", context)

    else:
        name = request.POST.get("name")

        if Product.objects.filter(name__iexact=name).exists():
            messages.error(request, "O produto que deseja criar já existe!")
            return redirect("product_list")

        price = request.POST.get("price")
        ingredients_ids = request.POST.getlist("ingredients")

        ingredients_to_create = []

        for ingredient_id in ingredients_ids:
            try:
                quantity = float(request.POST.get(f"q-{ingredient_id}"))
            except ValueError:
                ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
                messages.error(request, f"Forneça uma quantidade válida para o ingrediente {ingredient_name}!")
                return redirect("product_list")

            ingredients_to_create.append((int(ingredient_id), quantity))

        product = Product.objects.create(name=name, price=price)

        for ingredient_id, quantity in ingredients_to_create:
            ProductIngredient.objects.create(
                product=product,
                ingredient_id=ingredient_id,
                quantity=quantity,
            )

        messages.success(request, "Produto criado com sucesso!")
        return redirect("product_list")


@login_required
@admin_required
@require_http_methods(["GET"])
def product_list(request):
    products = Product.objects.all()

    field = request.GET.get("field")
    value = request.GET.get("value")

    if field and value:
        if field == "name":
            products = products.filter(name__icontains=value)
        elif field == "price":
            try:
                value = float(value)
            except ValueError:
                messages.error(request, "Insira um número válido!")
                return redirect("product_list")

            products = products.filter(price=value)

    context = {
        "products": products,
        "field": field,
        "value": value,
    }

    return render(request, "product_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
        "product": product,
        "products_ingredients": product.productingredient_set.all(),
    }
    return render(request, "product_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def product_update(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "GET":
        context = {
            "product": product,
            "ingredients": Ingredient.objects.all(),
            "product_ingredients": product.productingredient_set.all(),
        }
        return render(request, "product_update.html", context)

    else:
        name = request.POST.get("name")

        if Product.objects.filter(name__iexact=name).exclude(id=product.id).exists():
            messages.error(request, "O novo nome que deseja inserir já está associado a um produto!")
            return redirect("product_list")

        price = request.POST.get("price")
        selected_ids = request.POST.getlist("ingredients")

        product.name = name
        product.price = price
        product.save(update_fields=["name", "price"])

        old_ingredients_ids = set(product.productingredient_set.values_list("ingredient_id", flat=True))
        new_ingredients_ids = set(int(pk) for pk in selected_ids)

        ids_to_remove = old_ingredients_ids - new_ingredients_ids

        if ids_to_remove:
            ProductIngredient.objects.filter(product=product, ingredient_id__in=ids_to_remove).delete()

        for ingredient_id in new_ingredients_ids:
            try:
                quantity = float(request.POST.get(f"q-{ingredient_id}"))
            except ValueError:
                ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
                messages.error(request, f"Forneça uma quantidade válida para o ingrediente {ingredient_name}")
                return redirect("product_list")

            ProductIngredient.objects.update_or_create(
                product=product,
                ingredient_id=ingredient_id,
                quantity=quantity,
            )

        messages.success(request, "Produto alterado com sucesso!")
        return redirect("product_list")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "GET":
        context = {"product": product}
        return render(request, "product_delete.html", context)

    else:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            messages.error(request, "A senha que você inseriu está incorreta!")
            return redirect("product_list")

        product.delete()

        messages.success(request, "Produto deletado com sucesso!")
        return redirect("product_list")
