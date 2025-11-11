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
    # Service record URLs
    path("service/add/", views.ServiceRecordCreateView.as_view(), name="service_add"),
    path(
        "service/update/<int:pk>/",
        views.ServiceRecordUpdateView.as_view(),
        name="service_update",
    ),
    path(
        "service/<int:pk>/delete/",
        views.ServiceRecordDeleteView.as_view(),
        name="service_delete",
    ),
]
