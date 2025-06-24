from django.urls import path

from .views import delete_account, detail_account, list_account, login, register, update_account

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("", list_account, name="list"),
    path("<int:id>", detail_account, name="detail"),
    path("<int:id>/update", update_account, name="update"),
    path("<int:id>/delete", delete_account, name="delete"),
]
