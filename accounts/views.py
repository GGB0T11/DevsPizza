from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.decorators import admin_required

from .models import CustomUser


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


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        context = {"role_choices": CustomUser._meta.get_field("role").choices}
        return render(request, "register.html", context)

    else:
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            role = request.POST.get("role")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if CustomUser.objects.filter(email=email):
                raise Exception("Já existe um usuário cadastrado com esse email, insira outro")

            if password != confirm_password:
                raise Exception("As senhas devem ser iguais!")

            if len(password) < 8:
                raise Exception("A senha deve ter no mínimo 8 caracteres!")

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
            return redirect("account_list")

        except Exception as e:
            messages.error(request, str(e))
            context = context = {"role_choices": CustomUser._meta.get_field("role").choices, "old_data": request.POST}
            return render(request, "register.html", context)


@login_required
@require_http_methods(["POST"])
def logout(request):
    logout_django(request)
    messages.success(request, "Deslogado com sucesso!")
    return redirect("register")


@login_required
@admin_required
@require_http_methods(["GET"])
def account_list(request):
    accounts = CustomUser.objects.all()

    field = request.GET.get("field")
    value = request.GET.get("value")

    if field and value:
        if field == "first_name":
            accounts = accounts.filter(first_name__icontains=value)
        elif field == "email":
            accounts = accounts.filter(email=value)
        elif field == "role":
            accounts = accounts.filter(role=value)

    context = {
        "accounts": accounts,
        "role_choices": CustomUser._meta.get_field("role").choices,
        "field": field,
        "value": value,
    }
    return render(request, "account_list.html", context)


@login_required
@admin_required
@require_http_methods(["GET"])
def account_detail(request, id):
    account = get_object_or_404(CustomUser, id=id)

    context = {"account": account}
    return render(request, "account_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def account_update(request, id):
    account = get_object_or_404(CustomUser, id=id)
    context = {"account": account, "role_choices": CustomUser._meta.get_field("role").choices}

    if request.method == "GET":
        return render(request, "account_update.html", context)

    else:
        try:
            email = request.POST.get("email")

            if CustomUser.objects.filter(email=email).exclude(id=account.id).exists():
                raise Exception("O novo email que deseja inserir já está associado a uma conta!")

            account.first_name = request.POST.get("first_name")
            account.last_name = request.POST.get("last_name")
            account.email = email
            account.role = request.POST.get("role")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password and confirm_password:
                if password == confirm_password:
                    if len(password) >= 8:
                        account.set_password(request.POST.get("password"))
                    else:
                        raise Exception("A senha deve ter no mínimo 8 caracteres")
                else:
                    raise Exception("As senhas não coincidem!")

            account.save()

            messages.success(request, "Conta alterada com sucesso!")
            return redirect("account_list")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, "account_update.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def account_delete(request, id):
    account = get_object_or_404(CustomUser, id=id)

    if request.method == "GET":
        context = {"account": account}
        return render(request, "account_delete.html", context)

    else:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            messages.error(request, "A senha que você inseriu está incorreta!")
            return redirect("account_list")

        account.delete()

        messages.success(request, "Conta deletada com sucesso!")
        return redirect("account_list")
