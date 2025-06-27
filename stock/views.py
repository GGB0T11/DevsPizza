from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Category, Ingredient, Product


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

        return render(request, "ingredient_create", {"categories": categories})

    else:
        return       

    return
