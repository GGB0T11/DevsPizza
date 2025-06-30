from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("", views.list_account, name="list"),
    # path("", AccountListView.as_view(), name="list"),
    path("<int:id>", views.detail_account, name="detail"),
    path("<int:id>/update", views.update_account, name="update"),
    path("<int:id>/delete", views.delete_account, name="delete"),
]
