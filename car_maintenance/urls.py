from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),  # Login, logout, password reset
    path("auth/", include("registration.urls")),  # Registration
    path("vehicles/", include("vehicles.urls")),
    path("", home_view, name="home"),  # Landing page
]
