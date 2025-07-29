from django.urls import path

from . import views

urlpatterns = [
    path("new/", views.movement_create, name="movement_create"),
    path("", views.movement_list, name="movement_list"),
    path("<int:id>", views.movement_detail, name="movement_detail"),
    path("<int:id>/delete", views.movement_delete, name="movement_delete"),
    path("report", views.report, name="report"),
]
