from decimal import Decimal, InvalidOperation

from core.decorators import admin_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Category, Ingredient, Product, ProductIngredient


def parse_value_br(value: str) -> Decimal:
    """
    Converte valor no formato brasileiro (1.234,56)
    para Decimal no padrão internacional (1234.56).
    """

    try:
        value = value.replace(".", "")
        value = value.replace(",", ".")
        return Decimal(value)
    except InvalidOperation:
        raise ValueError("Insira um valor válido!")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def category_create(request: HttpRequest) -> HttpResponse:
    """Cria uma nova categoria.

    GET:
        Renderiza o formulário de criação de categoria.

    POST:
        - Cria uma nova categoria se o nome não existir.
        - Caso já exista, redireciona para a lista exibindo mensagem de erro.

    Returns:
        HttpResponse: Página de criação (GET ou POST inválido).
        HttpResponseRedirect: Redireciona para a lista de categorias após criação ou erro.
    """

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
def category_list(request: HttpRequest) -> HttpResponse:
    """Lista todas as categorias cadastradas, com paginação.

    GET:
        Renderiza a lista paginada de categorias.

    Returns:
        HttpResponse: Página com a lista de categorias.
    """

    categories = Category.objects.all()

    page_number = request.GET.get("page") or 1
    paginator = Paginator(categories, 10)

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "Paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
    }
    return render(request, "category_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def category_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Exibe os detalhes de uma categoria específica.

    Args:
        id (int): Identificador único da categoria.

    GET:
        Renderiza a página de detalhes da categoria.

    Returns:
        HttpResponse: Página com os detalhes da categoria.
    """

    context = {"category": get_object_or_404(Category, id=id)}

    return render(request, "category_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def category_update(request: HttpRequest, id: int) -> HttpResponse:
    """Atualiza uma categoria existente.

    Args:
        id (int): Identificador único da categoria.

    GET:
        Renderiza o formulário com os dados atuais da categoria.

    POST:
        - Atualiza nome e descrição.
        - Caso o nome já exista em outra categoria, exibe mensagem de erro.

    Returns:
        HttpResponse: Página de edição (GET ou POST inválido).
        HttpResponseRedirect: Redireciona para a lista de categorias após atualização.
    """

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
def category_delete(request: HttpRequest, id: int) -> HttpResponse:
    """Exclui uma categoria existente.

    Args:
        id (int): Identificador único da categoria.

    GET:
        Renderiza a página de confirmação da exclusão.

    POST:
        - Valida a senha do usuário autenticado.
        - Remove a categoria se a senha for correta.

    Returns:
        HttpResponse: Página de confirmação de exclusão (GET).
        HttpResponseRedirect: Redireciona para a lista após exclusão ou erro de senha.
    """

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
def ingredient_create(request: HttpRequest) -> HttpResponse:
    """Cria um novo ingrediente.

    GET:
        Renderiza o formulário de criação de ingrediente.

    POST:
        - Cria um ingrediente associado a uma categoria.
        - Valida nome único, quantidades e medida.
        - Caso algum dado seja inválido, retorna o formulário preenchido com erros.

    Returns:
        HttpResponse: Página de criação (GET ou POST inválido).
        HttpResponseRedirect: Redireciona para a lista de ingredientes após criação.
    """

    if request.method == "GET":
        context = {
            "categories": Category.objects.all(),
            "measure_choices": Ingredient._meta.get_field("measure").choices,
        }
        return render(request, "ingredient_create.html", context)

    else:
        try:
            name = request.POST.get("name")
            category_id = request.POST.get("category")
            measure = request.POST.get("measure")

            category = get_object_or_404(Category, id=category_id)

            if Ingredient.objects.filter(name__iexact=name).exists():
                raise Exception("O ingrediente que deseja cadastrar já existe!")

            qte = request.POST.get("qte")
            qte = parse_value_br(qte)

            min_qte = request.POST.get("min_qte")
            min_qte = parse_value_br(min_qte)

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

        except Exception as e:
            messages.error(request, str(e))
            context = {
                "categories": Category.objects.all(),
                "measure_choices": Ingredient._meta.get_field("measure").choices,
                "old_data": request.POST,
            }
            return render(request, "ingredient_create.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def ingredient_list(request: HttpRequest) -> HttpResponse:
    """Lista todos os ingredientes cadastrados, com filtros e paginação.

    GET:
        - Permite filtrar por nome, categoria, quantidade ou quantidade mínima.
        - Renderiza a lista paginada de ingredientes.

    Returns:
        HttpResponse: Página com a lista de ingredientes.
    """

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

    page_number = request.GET.get("page") or 1
    paginator = Paginator(ingredients, 10)

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "Paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "categories": categories,
        "field": field,
        "value": value,
    }
    return render(request, "ingredient_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def ingredient_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Exibe os detalhes de um ingrediente específico.

    Args:
        id (int): Identificador único do ingrediente.

    GET:
        Renderiza a página de detalhes do ingrediente.

    Returns:
        HttpResponse: Página com os detalhes do ingrediente.
    """

    context = {"ingredient": get_object_or_404(Ingredient, id=id)}
    return render(request, "ingredient_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def ingredient_update(request: HttpRequest, id: int) -> HttpResponse:
    """Atualiza um ingrediente existente.

    Args:
        id (int): Identificador único do ingrediente.

    GET:
        Renderiza o formulário com os dados atuais do ingrediente.

    POST:
        - Atualiza nome, categoria, quantidades e medida.
        - Valida nome único e valores numéricos.
        - Caso algum dado seja inválido, exibe mensagem de erro.

    Returns:
        HttpResponse: Página de edição (GET ou POST inválido).
        HttpResponseRedirect: Redireciona para a lista de ingredientes após atualização.
    """

    ingredient = get_object_or_404(Ingredient, id=id)
    context = {
        "ingredient": ingredient,
        "categories": Category.objects.all(),
        "measure_choices": Ingredient._meta.get_field("measure").choices,
    }
    if request.method == "GET":
        return render(request, "ingredient_update.html", context)

    else:
        try:
            name = request.POST.get("name")

            if Ingredient.objects.filter(name__iexact=name).exclude(id=ingredient.id).exists():
                raise Exception("O novo nome que deseja inserir já está associado a um ingrediente")

            qte = request.POST.get("qte")
            qte = parse_value_br(qte)

            min_qte = request.POST.get("min_qte")
            min_qte = parse_value_br(min_qte)

            ingredient.name = name
            category_id = request.POST.get("category")
            ingredient.category = get_object_or_404(Category, id=category_id)
            ingredient.qte = qte
            ingredient.min_qte = min_qte
            ingredient.measure = request.POST.get("measure")

            ingredient.save()

            messages.success(request, "Ingrediente alterado com sucesso!")
            return redirect("ingredient_list")

        except Exception as e:
            messages.error(request, str(e))
            return render(request, "ingredient_update.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def ingredient_delete(request: HttpRequest, id: int) -> HttpResponse:
    """Exclui um ingrediente existente.

    Args:
        id (int): Identificador único do ingrediente.

    GET:
        Renderiza a página de confirmação da exclusão.

    POST:
        - Valida a senha do usuário autenticado.
        - Remove o ingrediente se a senha for correta.

    Returns:
        HttpResponse: Página de confirmação (GET).
        HttpResponseRedirect: Redireciona para a lista após exclusão ou erro de senha.
    """

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
def product_create(request: HttpRequest) -> HttpResponse:
    """Cria um novo produto com ingredientes associados.

    GET:
        Renderiza o formulário de criação de produto.

    POST:
        - Cria o produto com nome, preço e ingredientes.
        - Valida nome único, preço e quantidades.
        - Caso algum dado seja inválido, retorna o formulário preenchido com erros.

    Returns:
        HttpResponse: Página de criação (GET ou POST inválido).
        HttpResponseRedirect: Redireciona para a lista de produtos após criação.
    """

    context = {"ingredients": Ingredient.objects.all()}

    if request.method == "GET":
        return render(request, "product_create.html", context)

    else:
        try:
            name = request.POST.get("name")

            if Product.objects.filter(name__iexact=name).exists():
                raise Exception("O produto que deseja criar já existe!")

            try:
                price = request.POST.get("price")
            except ValueError:
                raise Exception("Insira um preço válido!")

            ingredients_ids = request.POST.getlist("ingredients")

            ingredients_to_create = []

            for ingredient_id in ingredients_ids:
                try:
                    quantity = float(request.POST.get(f"q-{ingredient_id}"))
                except ValueError:
                    ingredient_name = Ingredient.objects.get(pk=ingredient_id).name
                    raise Exception(f"Forneça uma quantidade válida para o ingrediente {ingredient_name}!")

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

        except Exception as e:
            messages.error(request, str(e))
            return render(request, "product_create.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def product_list(request: HttpRequest) -> HttpResponse:
    """Lista todos os produtos cadastrados, com filtros e paginação.

    GET:
        - Permite filtrar por nome ou preço.
        - Renderiza a lista paginada de produtos.

    Returns:
        HttpResponse: Página com a lista de produtos.
    """

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

    page_number = request.GET.get("page") or 1
    paginator = Paginator(products, 10)

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "Paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "field": field,
        "value": value,
    }

    return render(request, "product_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def product_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Exibe os detalhes de um produto específico, incluindo seus ingredientes.

    Args:
        id (int): Identificador único do produto.

    GET:
        Renderiza a página de detalhes do produto.

    Returns:
        HttpResponse: Página com os detalhes do produto.
    """

    product = get_object_or_404(Product, id=id)
    context = {
        "product": product,
        "products_ingredients": product.productingredient_set.all(),
    }
    return render(request, "product_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def product_update(request: HttpRequest, id: int) -> HttpResponse:
    """Atualiza um produto existente e seus ingredientes.

    Args:
        id (int): Identificador único do produto.

    GET:
        Renderiza o formulário com os dados atuais do produto.

    POST:
        - Atualiza nome, preço e ingredientes associados.
        - Valida nome único, preço e quantidades.
        - Adiciona ou remove ingredientes conforme seleção.

    Returns:
        HttpResponse: Página de edição (GET ou POST inválido).
        HttpResponseRedirect: Redireciona para a lista de produtos após atualização.
    """

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
def product_delete(request: HttpRequest, id: int) -> HttpResponse:
    """Exclui um produto existente.

    Args:
        id (int): Identificador único do produto.

    GET:
        Renderiza a página de confirmação da exclusão.

    POST:
        - Valida a senha do usuário autenticado.
        - Remove o produto se a senha for correta.

    Returns:
        HttpResponse: Página de confirmação (GET).
        HttpResponseRedirect: Redireciona para a lista após exclusão ou erro de senha.
    """

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
