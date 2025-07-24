from django.urls import path

from . import views

urlpatterns = [
    path("category/new", views.category_create, name="category_create"),
    path("category/", views.category_list, name="category_list"),
    path("category/<int:id>", views.category_detail, name="category_detail"),
    path("category/<int:id>/update", views.category_update, name="category_update"),
    path("category/<int:id>/delete", views.category_delete, name="category_delete"),
    path("ingredient/new", views.ingredient_create, name="ingredient_create"),
    path("ingredient/", views.ingredient_list, name="ingredient_list"),
    path("ingredient/<int:id>", views.ingredient_detail, name="ingredient_detail"),
    path("ingredient/<int:id>/update", views.ingredient_update, name="ingredient_update"),
    path("ingredient/<int:id>/delete", views.ingredient_delete, name="ingredient_delete"),
    path("product/new", views.product_create, name="product_create"),
    path("product/", views.product_list, name="product_list"),
    path("product/<int:id>", views.product_detail, name="product_detail"),
    path("product/<int:id>/update", views.product_update, name="product_update"),
    path("product/<int:id>/delete", views.product_delete, name="product_delete"),
]
