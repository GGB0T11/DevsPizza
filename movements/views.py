from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import AdminRequiredMixin, LoginRequiredMixin
from stock.models import Product

from .models import Movement
from .services import create_outflow


class MovementCreate(LoginRequiredMixin, CreateView):
    model = Movement
    fields = ["product", "transaction_type", "amount", "commentary"]
    template_name = "movement_create.html"

    def form_valid(self, form):
        user = self.request.user
        product = form.cleaned_data["product"]
        amount = form.cleaned_data["amount"]
        commentary = form.cleaned_data["commentary"]

        if form.cleaned_data["transaction_type"] == "outflow":
            try:
                self.object = create_outflow(user, product, amount, commentary)
            except ValueError as e:
                messages.error(self.request, e.messages[0])
                return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, "Movimentação registrada com sucesso!")
        return reverse("movement_list")


class MovementList(LoginRequiredMixin, ListView):
    model = Movement
    template_name = "movement_list.html"
    context_object_name = "movements"


class MovementDetail(LoginRequiredMixin, DetailView):
    model = Movement
    template_name = "movement_detail.html"
    context_object_name = "movement"


class MovementUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    fields = ["product", "type", "amount", "commentary"]
    model = Movement
    template_name = "movement_update.html"
    context_object_name = "movement"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, "Movimentação alterada com sucesso!")
        return reverse("movement_list")


class MovementDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Movement
    template_name = "movement_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Movimentação deletada com sucesso!")
        return reverse("movement_list")
