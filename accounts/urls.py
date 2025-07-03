from django.urls import path

from .views import AccountDelete, AccountDetail, AccountList, AccountLogin, logout, register, update_account

urlpatterns = [
    path("login/", AccountLogin.as_view(), name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("", AccountList.as_view(), name="account_list"),
    path("<int:pk>", AccountDetail.as_view(), name="account_detail"),
    path("<int:id>/update", update_account, name="account_update"),
    path("<int:pk>/delete", AccountDelete.as_view(), name="account_delete"),
]
