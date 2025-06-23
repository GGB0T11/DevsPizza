from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import CustomUser


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
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


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    else:
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
