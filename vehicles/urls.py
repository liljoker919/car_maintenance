from django.urls import path
from .views import (
    VehicleListView,
    VehicleCreateView,
)

urlpatterns = [
    path("", VehicleListView.as_view(), name="vehicle_list"),
    path("add/", VehicleCreateView.as_view(), name="vehicle_add"),
]
