from django.urls import path

from .views import MovementCreate

urlpatterns = [
    path("new", MovementCreate.as_view(), name="create"),
    # path("", views.movements_list, name="list"),
    # path("<int:id>", views.movements_detail, name="detail"),
    # path("<int:id>/update", views.movements_update, name="update"),
    # path("<int:id>/delete", views.movements_delete, name="delete"),
]
