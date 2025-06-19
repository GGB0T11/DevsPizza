from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Usuario



@require_http_methods(["GET", "POST"])
def criar_usuario(request):
    print(request)
    if request.method == "GET":
        return render(request, "criar_usuario.html")
    

    email = request.POST.get("email")
    nome = request.POST.get("nome")
    password =request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    sobrenome = request.POST.get("sobrenome")
    cargo = request.POST.get("cargo")

    if Usuario.objects.filter(email=email).exists():
        messages.error(request, "O email inserido já existe")
        return redirect("criar_usuario")
    
    if password != confirm_password:
        messages.error(request, "Os dois campos de senha não correspondem.")
        return redirect("criar_usuario")

    if len(password) < 8:
        messages.error(request, "A senha deve ter no mínimo 8 caracteres")
        return redirect("criar_usuario")
    
    Usuario.objects.create_user(
        email=email,
        nome=nome,
        sobrenome=sobrenome,
        password=password,
        cargo=cargo
    )