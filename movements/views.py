from django.contrib import messages
from django.shortcuts import redirect, render
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

        messages.success(request, "Movimentação registrada com sucesso!")
        return redirect("list")


class MovementList(ListView):
    model = Movement
    template_name = "movement_list.html"
    context_object_name = "movements"


class MovementDetail(DetailView):
    model = Movement
    template_name = "movement_detail.html"
    context_object_name = "movement"


class MovementUpdate(UpdateView):
    model = Movement
    template_name = "movement_update.html"
    context_object_name = "movements"

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        context["products"] = Product.objects.all()

        return context
