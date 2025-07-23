from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("", views.account_list, name="account_list"),
    path("<int:id>", views.account_detail, name="account_detail"),
    path("<int:id>/update", views.account_update, name="account_update"),
    path("<int:id>/delete", views.account_delete, name="account_delete"),
]
