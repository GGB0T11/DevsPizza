from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from stock.models import Product

from .models import Movement


class MovementCreate(View):
    template_name = "movement_create.html"

    def get(self, request):
        products = Product.objects.all()
        return render(request, self.template_name, {"products": products})

    def post(self, request):
        product_id = request.POST.get("product")
        movement_type = request.POST.get("type")
        print(movement_type)
        amount = request.POST.get("amount")
        commentary = request.POST.get("commentary")

        product = Product.objects.get(id=product_id)
        user = request.user

        Movement.objects.create(product=product, user=user, type=movement_type, amount=amount, commentary=commentary)

    def get_success_url(self):
        messages.success(self.request, "Movimentação registrada com sucesso!")
        return reverse("movement_list")


class MovementList(ListView):
    model = Movement
    template_name = "movement_list.html"
    context_object_name = "movements"


class MovementDetail(DetailView):
    model = Movement
    template_name = "movement_detail.html"
    context_object_name = "movement"


# TODO: Passar os fields
class MovementUpdate(UpdateView):
    fields = []
    model = Movement
    template_name = "movement_update.html"
    context_object_name = "movements"

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        context["products"] = Product.objects.all()

        return context


class MovementDelete(DeleteView):
    model = Movement
    template_name = "movement_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Movimantação deletada com sucesso!")
        return reverse("movement_list")
