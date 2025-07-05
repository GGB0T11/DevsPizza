from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import AdminRequiredMixin, LoginRequiredMixin

from .models import Category, Ingredient, Product


class CategoryCreate(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Category
    fields = ["name", "description"]
    template_name = "category_create.html"

    def get_success_url(self):
        messages.success(self.request, "Categoria registrada com sucesso!")
        return reverse("category_list")


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"


class CategoryDetail(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"


class CategoryUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    fields = ["name", "description"]
    model = Category
    template_name = "category_update.html"
    context_object_name = "category"

    def get_success_url(self):
        messages.success(self.request, "Categoria alterada com sucesso!")
        return reverse("category_list")


class CategoryDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Category
    template_name = "category_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Categoria deletada com sucesso!")
        return reverse("category_list")


class IngredientCreate(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Ingredient
    fields = ["name", "category", "current_qte", "measure_unit"]
    template_name = "ingredient_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, "Ingrediente registrado com sucesso!")
        return reverse("ingredient_list")


class IngredientList(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "ingredient_list.html"
    context_object_name = "ingredients"


class IngredientDetail(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Ingredient
    template_name = "ingredient_detail.html"
    context_object_name = "ingredient"


class IngredientUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    fields = ["name", "category", "current_qte", "measure_unit", "active"]
    model = Ingredient
    template_name = "ingredient_update.html"
    context_object_name = "ingredient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, "Ingrediente alterado com sucesso!")
        return reverse("ingredient_list")


class IngredientDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "ingredient_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Ingrediente deletado com sucesso!")
        return reverse("ingredient_list")


class ProductCreate(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Product
    fields = ["name", "ingredients"]
    template_name = "product_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, "Produto registrado com sucesso!")
        return reverse("product_list")


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


class ProductDetail(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    fields = ["name", "ingredients"]
    model = Product
    template_name = "product_update.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, "Produto alterado com sucesso!")
        return reverse("product_list")


class ProductDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Produto deletado com sucesso!")
        return reverse("product_list")
