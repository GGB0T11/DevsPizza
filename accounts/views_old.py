from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import AdminRequiredMixin, CustomLoginRequiredMixin

from .models import CustomUser

# TODO: Tratar o erro 404


class AccountLogin(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Email ou senha inválidos")
        return super().form_invalid(form)


# TODO: Fazer verificações mais rígidas (letras, numeros, caracteres especiais)
# NOTE: tem como melhorar
class AccountRegister(CustomLoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = CustomUser
    fields = ["first_name", "last_name", "email", "role"]
    template_name = "register.html"
    success_url = reverse_lazy("account_list")

    def post(self, request):
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
        return redirect(self.success_url)


class AccountLogout(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Deslogado com sucesso!")
        return super().dispatch(request, *args, **kwargs)


class AccountList(CustomLoginRequiredMixin, AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "account_list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        queryset = super().get_queryset()
        value = self.request.GET.get("value")
        field = self.request.GET.get("field")

        if value and field:
            if field == "first_name":
                queryset = queryset.filter(first_name=value)
            elif field == "email":
                queryset = queryset.filter(email=value)
            elif field == "role":
                queryset = queryset.filter(role=value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["role_choices"] = CustomUser._meta.get_field("role").choices
        return context


class AccountDetail(CustomLoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = CustomUser
    template_name = "account_detail.html"
    context_object_name = "account"


# TODO: Tem que adicionar check password
# TODO: Apenas mostrar o email, não pode alterar
class AccountUpdate(CustomLoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["first_name", "last_name", "email", "role"]
    template_name = "account_update.html"
    context_object_name = "account"
    success_url = reverse_lazy("account_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password:
            if password != confirm_password:
                messages.error(request, "As senhas devem ser iguais!")
                return redirect(request.path)

            if len(password) < 8:
                messages.error(request, "A senha deve ter no mínimo 8 caracteres")
                return redirect(request.path)

            self.object.set_password(password)

        self.object.first_name = first_name
        self.object.last_name = last_name
        self.object.email = email
        self.object.role = role
        self.object.save()

        messages.success(request, "Conta alterada com sucesso!")
        return redirect(self.success_url)


class AccountDelete(CustomLoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "account_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Conta deletada com sucesso!")
        return reverse("account_list")
