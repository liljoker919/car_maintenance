from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("registration.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("", home_view, name="home"),  # Map root URL to home_view
]
