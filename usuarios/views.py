from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.views.decorators.http import require_http_methods
from .models import Usuario

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    else:
        nome_usuario = request.POST.get("nome_usuario")
        senha = request.POST.get("senha")

        usuario = authenticate(username=nome_usuario, password=senha)

        if usuario:
            login_django(request, usuario)
            return redirect("home")
        
        else:
            messages.error(request, "Nome de Usuario ou senha inválidos")
            return redirect("login")

@require_http_methods(["GET", "POST"])
def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")

    else:
        nome_usuario = request.POST.get("nome_usuario")
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")
        cargo = request.POST.get("cargo")

        if Usuario.objects.filter(username=nome_usuario):
            messages.error(request, "Esse nome de usuário já esta em uso, insira outro")
            redirect("cadastro")

        if Usuario.objects.filter(email=email):
            messages.error(request, "já existe uma conte vinculada a esse email, insira outro")
            redirect("cadastro")

        if senha != confirmar_senha:
            messages.error(request, "As senhas deve ser iguais")
            redirect("cadastro")

        if len(senha) < 8:
            messages.error(request, "A senha deve ter no minimo 8 caracteres")
            redirect("cadastro")

        usuario = Usuario.objects.create_user(
            username = nome_usuario,
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            password=senha,
            cargo=cargo
        )

        messages.success(request, "Usuário criado com sucesso")
        return redirect("home")
