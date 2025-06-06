from django.urls import path
from .views import (
    VehicleListView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
)

urlpatterns = [
    path("", VehicleListView.as_view(), name="vehicle_list"),
    path("add/", VehicleCreateView.as_view(), name="vehicle_add"),
    path("<int:pk>/edit/", VehicleUpdateView.as_view(), name="vehicle_edit"),
    path("<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle_delete"),
]
