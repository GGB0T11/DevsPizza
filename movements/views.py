from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from stock.models import Product

from .models import Movement


class MovementCreate(CreateView):
    model = Movement
    fields = ["product", "type", "amount", "commentary"]
    template_name = "movement_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context

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


class MovementUpdate(UpdateView):
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


class MovementDelete(DeleteView):
    model = Movement
    template_name = "movement_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Movimentação deletada com sucesso!")
        return reverse("movement_list")
