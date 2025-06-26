from django.urls import path

from .views import category_create, category_delete, category_detail, category_list, category_update

urlpatterns = [
    path("category/new", category_create, name="category_create"),
    path("category/", category_list, name="category_list"),
    path("category/<int:id>", category_detail, name="category_detail"),
    path("category/<int:id>/update", category_update, name="category_update"),
    path("category/<int:id>/delete", category_delete, name="category_delete"),
]
