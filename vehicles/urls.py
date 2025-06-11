from django.urls import path
from . import views
from .views import VehicleDetailView

urlpatterns = [
    path("list/", views.VehicleListView.as_view(), name="vehicle_list"),
    path(
        "add/", views.VehicleCreateView.as_view(), name="vehicle_add"
    ),  # ✅ Add this line
    path("update/<int:pk>/", views.VehicleUpdateView.as_view(), name="vehicle_update"),
    path("<int:pk>/delete/", views.VehicleDeleteView.as_view(), name="vehicle_delete"),
    path("<int:pk>/", VehicleDetailView.as_view(), name="vehicle_detail"),
]
