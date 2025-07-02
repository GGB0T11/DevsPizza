from django.urls import path

from .views import MovementCreate, MovementDelete, MovementDetail, MovementList, MovementUpdate

urlpatterns = [
    path("new/", MovementCreate.as_view(), name="movement_create"),
    path("", MovementList.as_view(), name="movement_list"),
    path("<int:pk>", MovementDetail.as_view(), name="movement_detail"),
    path("<int:pk>/update", MovementUpdate.as_view(), name="movement_update"),
    path("<int:pk>/delete", MovementDelete.as_view(), name="movement_delete"),
]
