from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import AdminRequiredMixin, LoginRequiredMixin

from .models import Category, Ingredient, Product, ProductIngredient
from .services import register_product, update_product


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
    fields = ["name", "category", "qte", "measure_unit"]
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

    def get_queryset(self):
        queryset = super().get_queryset()
        value = self.request.GET.get("value")
        field = self.request.GET.get("field")

        # NOTE: adicionar mais condicionais no filtro do qte
        if value and field:
            if field == "name":
                queryset = queryset.filter(name__icontains=value)
            elif field == "category":
                queryset = queryset.filter(category__icontains=value)
            elif field == "qte":
                queryset = queryset.filter(qte=value)

        return queryset


class IngredientDetail(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Ingredient
    template_name = "ingredient_detail.html"
    context_object_name = "ingredient"


class IngredientUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    fields = ["name", "category", "qte", "measure_unit", "active"]
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

    def form_valid(self, form):
        product_name = form.cleaned_data["name"]
        selected_ids = self.request.POST.getlist("ingredients")
        post_data = self.request.POST

        product_result = register_product(self.request, product_name, selected_ids, post_data)

        if product_result:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        if "name" in form.errors:
            messages.error(self.request, f"Já existe um produto com esse nome!")

        return super().form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Produto criado com sucesso!")
        return reverse("product_list")


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        value = self.request.GET.get("value")
        field = self.request.GET.get("field")

        if value and field:
            if field == "name":
                queryset = queryset.filter(name__icontains=value)
            elif field == "category":
                queryset = queryset.filter(category__icontains=value)

        return queryset


class ProductDetail(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["products_ingredients"] = product.productingredient_set.all()
        return context


class ProductUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Product
    fields = ["name", "ingredients"]
    template_name = "product_update.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        product = self.get_object()
        context["products_ingredients"] = product.productingredient_set.all()
        return context

    def form_valid(self, form):
        product_to_update = self.get_object()
        new_name = form.cleaned_data["name"]
        selected_ids = self.request.POST.getlist("ingredients")
        post_data = self.request.POST

        product_result = update_product(self.request, product_to_update, new_name, selected_ids, post_data)

        if product_result:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Produto alterado com sucesso!")
        return reverse("product_list")


class ProductDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Produto deletado com sucesso!")
        return reverse("product_list")
