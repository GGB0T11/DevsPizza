from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import CustomUser

# TODO: Tratar o erro 404
# TODO: Fazer o logout


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")

        else:
            return render(request, "login.html")

    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user:
            login_django(request, user)
            return redirect("home")

        else:
            messages.error(request, "Email ou senha inválidos")
            return redirect("login")


# TODO: Fazer verificações mais rígidas
@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.role != "admin":
        messages.error(request, "Somente admins podem criar novas contas!")
        return redirect("home")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if CustomUser.objects.filter(email=email):
            messages.error(request, "Já existe um usuário cadastrado com esse email, insira outro")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "As senhas devem ser iguais!")
            return redirect("register")

        if len(password) < 8:
            messages.error(request, "A senha deve ter no mínimo 8 caracteres!")
            return redirect("register")

        user = CustomUser.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            password=password,
        )

        user.save()

        messages.success(request, "Usuário criado com sucesso!")
        return redirect("home")

    return render(request, "register.html")


# TODO: Fazer paginação
@login_required
@require_http_methods(["GET"])
def list_account(request):
    if request.user.role != "admin":
        messages.error(request, "Somente admins podem ver os usuários!")
        return redirect("home")

    accounts = CustomUser.objects.all()

    return render(request, "list.html", {"accounts": accounts})


@login_required
@require_http_methods(["GET"])
def detail_account(request, id):
    if request.user.role != "admin":
        messages.error(request, "Somente admins podem ver detalhes das contas!")
        return redirect("home")

    account = get_object_or_404(CustomUser, id=id)

    return render(request, "detail.html", {"account": account})


# FIX: tem que poder trocar a senha com o set_password, se fode pra mostrar a senha bonita
@login_required
@require_http_methods(["GET", "POST"])
def update_account(request, id):
    if request.user.role != "admin":
        messages.error(request, "Somente admins podem alterar contas")
        return redirect("home")

    account = get_object_or_404(CustomUser, id=id)

    if request.method == "GET":
        return render(request, "update.html", {"account": account})

    else:
        account.first_name = request.POST.get("first_name")
        account.last_name = request.POST.get("last_name")
        account.email = request.POST.get("email")
        account.role = request.POST.get("role")

        account.save()

        messages.success(request, "Conta alterada com sucesso!")
        return redirect("list")


# Tailwind modal
# TODO: Solicitar confirmação
# NOTE: Não pode deletar a propria conta
@login_required
@require_http_methods(["GET", "POST"])
def delete_account(request, id):
    account = get_object_or_404(CustomUser, id=id)

    if request.user.role != "admin":
        messages.error(request, "Somente admins podem deletar contas")
        return redirect("home")

    if request.method == "POST":
        account.delete()

        messages.success(request, "Conta deletada com sucesso!")
        return redirect("list")

    return render(request, "delete.html", {"account": account})
