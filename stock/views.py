from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Category, Ingredient, Product

# TODO: Filtragem e busca nas lists
# TODO: 404 mais amigavel e detalhado


# TODO: Fazer formatação e validação no nome
@login_required
@require_http_methods(["GET", "POST"])
def category_create(request):
    print(request)
    if request.method == "GET":
        return render(request, "category_create.html")

    else:
        name = request.POST.get("name")
        description = request.POST.get("description")

        if Category.objects.filter(name=name):
            messages.error(request, "A categoria que deseja cadastrar já existe!")
            return redirect("category_list")

        category = Category.objects.create(name=name, description=description)

        category.save()

        messages.success(request, "Categoria criada com sucesso!")
        return redirect("category_list")


# TODO: Mostrar uma mensagem se não tiver categoria
@login_required
@require_http_methods(["GET"])
def category_list(request):
    categories = Category.objects.all()

    return render(request, "category_list.html", {"categories": categories})


@login_required
@require_http_methods(["GET"])
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)

    return render(request, "category_detail.html", {"category": category})


@login_required
@require_http_methods(["GET", "POST"])
def category_update(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "GET":
        return render(request, "category_update.html", {"category": category})

    else:
        category.name = request.POST.get("name")
        category.description = request.POST.get("description")

        category.save()

        messages.success(request, "Categoria alterada com sucesso!")
        return redirect("category_list")


@login_required
@require_http_methods(["GET"])
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)

    category.delete()

    messages.success(request, "Categoria deletada com sucesso!")
    return redirect("category_list")


@login_required
@require_http_methods(["GET", "POST"])
def ingredient_create(request):
    if request.method == "GET":
        categories = Category.objects.all()

        return render(request, "ingredient_create.html", {"categories": categories})

    else:
        name = request.POST.get("name")
        qte = request.POST.get("qte")
        category_id = request.POST.get("category")
        measure_unit = request.POST.get("measure_unit")

        category = get_object_or_404(Category, id=category_id)

        if Ingredient.objects.filter(name=name):
            messages.error(request, "O ingrediente que deseja cadastrar já existe!")
            return redirect("ingredient_list")

        ingredient = Ingredient.objects.create(name=name, current_qte=qte, category=category, measure_unit=measure_unit)

        ingredient.save()

        messages.success(request, "Ingrediente cadastrado com sucesso!")
        return redirect("ingredient_list")


@login_required
@require_http_methods(["GET"])
def ingredient_list(request):
    ingredients = Ingredient.objects.all()

    return render(request, "ingredient_list.html", {"ingredients": ingredients})


@login_required
@require_http_methods(["GET"])
def ingredient_detail(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)

    return render(request, "detail.html", {"ingredient": ingredient})


@login_required
@require_http_methods(["GET", "POST"])
def ingredient_update(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    categories = Category.objects.all()

    if request.method == "GET":
        return render(request, "ingredient_update.html", {"ingredient": ingredient, "categories": categories})

    else:
        ingredient.name = request.POST.get("name")
        category_id = request.POST.get("category")
        ingredient.category = get_object_or_404(Category, id=category_id)
        ingredient.measure_unit = request.POST.get("measure_unit")

        if request.POST.get("active") == "True":
            ingredient.active = True

        else:
            ingredient.active = False

        ingredient.save()

        messages.success(request, "Ingrediente alterado com sucesso!")
        return redirect("ingredient_list")


@login_required
@require_http_methods(["GET"])
def ingredient_delete(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)

    ingredient.delete()

    messages.success(request, "Ingrediente deletado com sucesso!")
    return redirect("ingredient_list")


@login_required
@require_http_methods(["GET", "POST"])
def product_create(request):
    if request.method == "GET":
        ingredients = Ingredient.objects.all()
        return render(request, "product_create.html", {"ingredients": ingredients})

    else:
        name = request.POST.get("name")
        ingredients_ids = request.POST.getlist("ingredients")
        ingredients = Ingredient.objects.filter(id__in=ingredients_ids)

        product = Product.objects.create(name=name)
        product.ingredients.set(ingredients)
        product.save()

        messages.success(request, "Produto criado com sucesso!")
        return redirect("product_list")


@login_required
@require_http_methods(["GET"])
def product_list(request):
    products = Product.objects.all()

    return render(request, "product_list.html", {"products": products})


@login_required
@require_http_methods(["GET"])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, "product_detail", {"product": product})


@login_required
@require_http_methods(["GET", "POST"])
def product_update(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "GET":
        ingredients = Ingredient.objects.all()
        ingredients_ids = product.ingredients.values_list("id", flat=True)

        return render(
            request,
            "product_update.html",
            {"product": product, "ingredients": ingredients, "ingredients_ids": ingredients_ids},
        )

    else:
        product.name = request.POST.get("name")
        ingredients_ids = request.POST.getlist("ingredients")
        ingredients = Ingredient.objects.filter(id__in=ingredients_ids)
        product.ingredients.set(ingredients)

        product.save()

        messages.success(request, "Produto alterado com sucesso!")
        return redirect("product_list")


@login_required
@require_http_methods(["GET"])
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    product.delete()

    messages.success(request, "Produto deletado com sucesso!")
    return redirect("product_list")
