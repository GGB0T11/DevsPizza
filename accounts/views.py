from django.contrib import messages
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from .models import CustomUser

# TODO: Tratar o erro 404


class AccountLogin(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Email ou senha inválidos")
        return super().form_invalid(form)


# FIX: Fazer essa porra em CBV
# TODO: Fazer verificações mais rígidas (letras, numeros, caracteres especiais)
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


# NOTE: Nao sei se vale a pena fazer isso em CBV
@login_required
@require_http_methods(["GET"])
def logout(request):
    logout_django(request)
    messages.success(request, "Deslogado com sucesso!")
    return redirect("register")


# TODO: Fazer paginação
class AccountList(ListView):
    model = CustomUser
    template_name = "account_list.html"
    context_object_name = "accounts"


class AccountDetail(DetailView):
    model = CustomUser
    template_name = "account_detail.html"
    context_object_name = "account"


# FIX: Refazer no formato CBV
# TODO: Tem que adicionar check password
@login_required
@require_http_methods(["GET", "POST"])
def update_account(request, id):
    if request.user.role != "admin":
        messages.error(request, "Somente admins podem alterar contas")
        return redirect("home")

    account = get_object_or_404(CustomUser, id=id)

    if request.method == "GET":
        return render(request, "account_update.html", {"account": account})

    else:
        account.first_name = request.POST.get("first_name")
        account.last_name = request.POST.get("last_name")
        account.email = request.POST.get("email")
        account.role = request.POST.get("role")
        password = request.POST.get("password")
        if password:
            account.set_password(request.POST.get("password"))

        account.save()

        messages.success(request, "Conta alterada com sucesso!")
        return redirect("account_list")


class AccountDelete(DeleteView):
    model = CustomUser
    template_name = "account_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Conta deletada com sucesso!")
        return reverse("account_list")
