from itertools import chain

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView, DetailView, UpdateView

from core.mixins import AdminRequiredMixin, LoginRequiredMixin
from stock.models import Ingredient, Product

from .models import Inflow, Outflow
from .services import create_inflow, create_outflow


class MovementCreate(LoginRequiredMixin, View):
    template_name = "movement_create.html"

    def get(self, request):
        context = {"products": Product.objects.all(), "ingredients": Ingredient.objects.all()}
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        commentary = request.POST.get("commentary")

        if request.POST.get("transaction_type") == "inflow":
            post_data = self.request.POST
            ingredients_ids = self.request.POST.getlist("ingredients")
            movement = create_inflow(request, user, ingredients_ids, commentary, post_data)

        else:
            product = request.POST.get("product")
            amount = request.POST.get("amount")
            movement = create_outflow(request, user, product, amount, commentary)

        if movement:
            messages.success(request, "Movimentação registrada com sucesso!")
            return redirect("movement_list")
        else:
            return redirect("movement_create")


class MovementList(LoginRequiredMixin, View):
    template_name = "movement_list.html"

    def get(self, request):
        inflow = Inflow.objects.all()
        outflow = Outflow.objects.all()

        combined = list(chain(inflow, outflow))
        sorted_combined = sorted(combined, key=lambda x: x.date, reverse=True)

        context = {"movements": sorted_combined}
        return render(request, self.template_name, context)


class MovementDetail(LoginRequiredMixin, DetailView):
    # model = Movement
    template_name = "movement_detail.html"
    context_object_name = "movement"


class MovementUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    fields = ["product", "type", "amount", "commentary"]
    # model = Movement
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
    # model = Movement
    template_name = "movement_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Movimentação deletada com sucesso!")
        return reverse("movement_list")
