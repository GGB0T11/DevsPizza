from itertools import chain

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView, UpdateView

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


# NOTE: Adicionar o filter aqui (data e user)
class MovementList(LoginRequiredMixin, View):
    template_name = "movement_list.html"

    def get(self, request):
        inflow = Inflow.objects.all()
        outflow = Outflow.objects.all()

        combined = list(chain(inflow, outflow))
        sorted_combined = sorted(combined, key=lambda x: x.date, reverse=True)

        context = {"movements": sorted_combined}
        return render(request, self.template_name, context)


class MovementDetail(LoginRequiredMixin, View):
    template_name = "movement_detail.html"

    def get(self, request, *args, **kwargs):
        transaction_type = self.kwargs["type"]
        movement_id = self.kwargs["id"]

        if transaction_type == "inflow":
            movement = Inflow.objects.get(pk=movement_id)
            ingredients = movement.inflowingredient_set.all() if isinstance(movement, Inflow) else None
            print(ingredients)
            context = {"movement": movement, "ingredients": ingredients}

        else:
            movement = Outflow.objects.get(pk=movement_id)
            context = {"movement": movement}

        return render(request, self.template_name, context)


class MovementUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = "movement_update.html"

    def get(self, request, *args, **kwargs):
        transaction_type = self.kwargs["type"]
        movement_id = self.kwargs["id"]

        if transaction_type == "inflow":
            movement = Inflow.objects.get(pk=movement_id)
        else:
            movement = Outflow.objects.get(pk=movement_id)

        context = {"movement": movement}

        return render(request, self.template_name, context)


class MovementDelete(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "movement_delete.html"

    def get(self, request, *args, **kwargs):
        transaction_type = self.kwargs["type"]
        movement_id = self.kwargs["id"]

        if transaction_type == "inflow":
            movement = Inflow.objects.get(pk=movement_id)

        else:
            movement = Outflow.objects.get(pk=movement_id)

        context = {"movement": movement}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        transaction_type = self.kwargs["type"]
        movement_id = self.kwargs["id"]

        if transaction_type == "inflow":
            movement = get_object_or_404(Inflow, id=movement_id)

        else:
            movement = get_object_or_404(Outflow, id=movement_id)

        movement.delete()

        messages.success(request, "Movimentação deletada com sucesso!")
        return redirect("movement_list")
