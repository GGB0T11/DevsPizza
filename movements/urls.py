from django.urls import path

from .views import MovementCreate, MovementDetail, MovementList, MovementUpdate

urlpatterns = [
    path("new/", MovementCreate.as_view(), name="create"),
    path("", MovementList.as_view(), name="list"),
    path("<int:pk>", MovementDetail.as_view(), name="detail"),
    path("<int:pk>/update", MovementUpdate.as_view(), name="update"),
    # path("<int:id>/delete", views.movements_delete, name="delete"),
]
