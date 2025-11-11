from django.contrib import admin
from django.urls import path, include
from .views import home_view
from vehicles.views import VehicleListView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("register/", include("registration.urls")),
    path("vehicles/", include(("vehicles.urls", "vehicles"), namespace="vehicles")),
    path("insurance/", include(("insurance.urls", "insurance"), namespace="insurance")),
    path(
        "compliance/",
        include(("compliance.urls", "compliance"), namespace="compliance"),
    ),
    path("", home_view, name="home"),
    path("my-garage/", VehicleListView.as_view(), name="vehicle_list"),  # ✅ Fixes E009
]
