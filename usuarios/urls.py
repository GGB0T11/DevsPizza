from django.urls import path
from .views import criar_usuario

urlpatterns = [
    path("criar/", criar_usuario, name="criar")
]