from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.decorators import admin_required

from .models import CustomUser
from .services import create_account, update_account


@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    """Renderiza a página de login e processa a autenticação do usuário.

    Args:
        request (HttpRequest): Objeto de requisição do Django.

    GET:
        Renderiza a tela de login com o formulário em branco.

    POST:
        Valida o email e a senha fornecidos:
            - Se válidos, redireciona para a página inicial (home).
            - Se inválidos, redireciona de volta para a página de login com uma mensagem de erro.

    Returns:
        HttpResponse: Página de login (GET ou POST com dados inválidos).
        HttpResponseRedirect: Redirecionamento para a página inicial (POST válido).
    """

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "login.html")

    email = request.POST.get("email")
    password = request.POST.get("password")

    if not email or not password:
        messages.error(request, "Preencha todos os campos")
        return render(request, "login.html", {"email": email})

    user = authenticate(email=email, password=password)

    if user:
        login_django(request, user)
        return redirect("home")
    messages.error(request, "Email ou senha inválidos")
    return render(request, "login.html", {"email": email})


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    """Renderiza a página de registro e processa o cadastro do usuário.

    Args:
        request (HttpRequest): Objeto de requisição do Django.

    GET:
        Renderiza a tela de registro com o formulário em branco.

    POST:
        Valida os campos fornecidos:
            - Se válidos, adiciona o novo usuário ao banco de dados e redireciona para a lista de usuários com uma mensagem confirmando a ação.
            - Se inválidos, redireciona novamente com uma mensagem de erro para a página de registro preenchida com os dados.

    Returns:
        HttpResponse: Página de registro (GET ou POST com dados inválidos).
        HttpResponseRedirect: Redirecionamento para a página a lista de usuários (POST válido).
    """

    context = {"role_choices": CustomUser._meta.get_field("role").choices}

    if request.method == "GET":
        return render(request, "register.html", context)

    try:
        user = create_account(request.POST)

        user.save()

        messages.success(request, "Usuário criado com sucesso!")
        return redirect("account_list")

    except ValidationError as e:
        for msg in e.messages:
            messages.error(request, msg)
        context["old_data"] = request.POST
        return render(request, "register.html", context)


@login_required
@require_http_methods(["POST"])
def logout(request: HttpRequest) -> HttpResponse:
    """Realiza o processo de logout do usuário.

    Args:
        request (HttpRequest): Objeto de requisição do Django.

    POST:
        Envia uma requisição solicitando o logout

    Returns:
        HttpResponseRedirect: Redirecionamento para a página de login.
    """

    logout_django(request)
    messages.success(request, "Deslogado com sucesso!")
    return redirect("login")


@login_required
@admin_required
@require_http_methods(["GET"])
def account_list(request: HttpRequest) -> HttpResponse:
    """Renderiza uma lista contendo os usuários do sistema.

    Args:
        request (HttpRequest): Objeto de requisição do Django.

    GET:
        Renderiza a tela de usuários com o filtro vazio:
            - Se tiver Filtro, retorna os elementos que correspondem ao Filtro.
            - Se não tiver, retorna os elementos de acordo com a página.

    Returns:
        HttpResponse: Página listando os usuários.
    """

    accounts = CustomUser.objects.all()

    field = request.GET.get("field")
    value = request.GET.get("value")

    if field and value:
        match field:
            case "first_name":
                accounts = accounts.filter(first_name__icontains=value)
            case "email":
                accounts = accounts.filter(email=value)
            case "role":
                accounts = accounts.filter(role=value)

    page_number = request.GET.get("page") or 1
    paginator = Paginator(accounts, 10)

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "Paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "role_choices": CustomUser._meta.get_field("role").choices,
        "field": field,
        "value": value,
    }
    return render(request, "account_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def account_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Renderiza uma página com detalhes do usuário.

    Args:
        request (HttpRequest): Objeto de requisição do Django.
        id (int): identificador único do usuário.

    GET:
        Renderiza a tela com os dados do usuário.

    Returns:
        HttpResponse: Página de detalhamento.
    """

    account = get_object_or_404(CustomUser, id=id)

    return render(request, "account_detail.html", {"account": account})


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def account_update(request: HttpRequest, id: int) -> HttpResponse:
    """Renderiza a página de atualização com os dados do usuário.

    Args:
        request (HttpRequest): Objeto de requisição do Django.
        id (int): identificador único do usuário.

    GET:
        Renderiza a tela de registro com o formulário preenchido com os dados do usuário.

    POST:
        Valida os campos fornecidos:
            - Se válidos, altera o usuário no banco de dados e redireciona para a lista de usuários com uma mensagem confirmando a ação .
            - Se inválidos, redireciona de volta para a página de alteração preenchida com os dados com uma mensagem de erro.

    Returns:
        HttpResponse: Página de registro (GET ou POST com dados inválidos).
        HttpResponseRedirect: Redirecionamento para a página a lista de usuários (POST válido).
    """

    account = get_object_or_404(CustomUser, id=id)
    context = {"account": account, "role_choices": CustomUser._meta.get_field("role").choices}

    if request.method == "GET":
        return render(request, "account_update.html", context)

    try:
        account = update_account(account, request.POST)

        account.save()

        messages.success(request, "Conta alterada com sucesso!")
        return redirect("account_list")
    except ValidationError as e:
        for msg in e.messages:
            messages.error(request, msg)
        return render(request, "account_update.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def account_delete(request, id):
    """Exibe e processa a exclusão do usuário.

    Args:
        request (HttpRequest): Objeto de requisição do Django.
        id (int): identificador único do usuário.

    GET:
        Renderiza a tela de deletar usuário solicitando senha.

    POST:
        Valida a senha:
            - Se válida, deleta usuário do do banco de dados com uma mensagem de sucesso.
            - Se inválido, redireciona para a página de insersão de senha com uma mensagem de erro.

    Returns:
        HttpResponse: Página de deletar usuário (senha inválida).
        HttpResponseRedirect: Redirecionamento para a página a lista de usuários (POST válido).
    """

    account = get_object_or_404(CustomUser, id=id)
    context = {"account": account}

    if request.method == "GET":
        return render(request, "account_delete.html", context)

    else:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            messages.error(request, "A senha que você inseriu está incorreta!")
            return render(request, "account_delete.html", context)

        account.delete()

        messages.success(request, "Conta deletada com sucesso!")
        return redirect("account_list")
