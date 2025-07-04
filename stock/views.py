from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Category, Ingredient, Product


class CategoryCreate(CreateView):
    model = Category
    fields = ["name", "description"]
    template_name = "category_create.html"

    def get_success_url(self):
        messages.success(self.request, "Categoria registrada com sucesso!")
        return reverse("category_list")


class CategoryList(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"


class CategoryDetail(DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"


class CategoryUpdate(UpdateView):
    fields = ["name", "description"]
    model = Category
    template_name = "category_update.html"
    context_object_name = "category"

    def get_success_url(self):
        messages.success(self.request, "Categoria alterada com sucesso!")
        return reverse("category_list")


class CategoryDelete(DeleteView):
    model = Category
    template_name = "category_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Categoria deletada com sucesso!")
        return reverse("category_list")


class IngredientCreate(CreateView):
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


class IngredientList(ListView):
    model = Ingredient
    template_name = "ingredient_list.html"
    context_object_name = "ingredients"


# FIX: Exibir os Ingredientes
class IngredientDetail(DetailView):
    model = Ingredient
    template_name = "ingredient_detail.html"
    context_object_name = "ingredient"


class IngredientUpdate(UpdateView):
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


class IngredientDelete(DeleteView):
    model = Ingredient
    template_name = "ingredient_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Ingrediente deletado com sucesso!")
        return reverse("ingredient_list")


class ProductCreate(CreateView):
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


class ProductList(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


class ProductDetail(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductUpdate(UpdateView):
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


class ProductDelete(DeleteView):
    model = Product
    template_name = "product_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Produto deletado com sucesso!")
        return reverse("product_list")
