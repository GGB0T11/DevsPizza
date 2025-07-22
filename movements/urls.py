from django.urls import path

from .views import MovementCreate, MovementDelete, MovementDetail, MovementList, MovementUpdate

urlpatterns = [
    path("new/", MovementCreate.as_view(), name="movement_create"),
    path("", MovementList.as_view(), name="movement_list"),
    path("<str:type>/<int:id>", MovementDetail.as_view(), name="movement_detail"),
    path("<str:type>/<int:id>/update", MovementUpdate.as_view(), name="movement_update"),
    path("<str:type>/<int:id>/delete", MovementDelete.as_view(), name="movement_delete"),
]
