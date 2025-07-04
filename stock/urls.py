from django.urls import path

from . import views

urlpatterns = [
    path("category/new", views.CategoryCreate.as_view(), name="category_create"),
    path("category/", views.CategoryList.as_view(), name="category_list"),
    path("category/<int:pk>", views.CategoryDetail.as_view(), name="category_detail"),
    path("category/<int:pk>/update", views.CategoryUpdate.as_view(), name="category_update"),
    path("category/<int:pk>/delete", views.CategoryDelete.as_view(), name="category_delete"),
    path("ingredient/new", views.IngredientCreate.as_view(), name="ingredient_create"),
    path("ingredient/", views.IngredientList.as_view(), name="ingredient_list"),
    path("ingredient/<int:pk>", views.IngredientDetail.as_view(), name="ingredient_detail"),
    path("ingredient/<int:pk>/update", views.IngredientUpdate.as_view(), name="ingredient_update"),
    path("ingredient/<int:pk>/delete", views.IngredientDelete.as_view(), name="ingredient_delete"),
    path("product/new", views.ProductCreate.as_view(), name="product_create"),
    path("product/", views.ProductList.as_view(), name="product_list"),
    path("product/<int:pk>", views.ProductDetail.as_view(), name="product_detail"),
    path("product/<int:pk>/update", views.ProductUpdate.as_view(), name="product_update"),
    path("product/<int:pk>/delete", views.ProductDelete.as_view(), name="product_delete"),
]
