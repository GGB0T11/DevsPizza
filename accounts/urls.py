from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.AccountLogin.as_view(), name="login"),
    path("register/", views.AccountRegister.as_view(), name="register"),
    path("logout/", views.AccountLogout.as_view(), name="logout"),
    path("", views.AccountList.as_view(), name="account_list"),
    path("<int:pk>", views.AccountDetail.as_view(), name="account_detail"),
    path("<int:pk>/update", views.AccountUpdate.as_view(), name="account_update"),
    path("<int:pk>/delete", views.AccountDelete.as_view(), name="account_delete"),
]
