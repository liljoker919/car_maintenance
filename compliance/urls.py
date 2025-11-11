from django.urls import path
from .views import (
    CarRegistrationCreateView,
    CarRegistrationUpdateView,
    CarRegistrationDeleteView,
)

urlpatterns = [
    path("add/", CarRegistrationCreateView.as_view(), name="registration_add"),
    path(
        "<int:pk>/edit/", CarRegistrationUpdateView.as_view(), name="registration_edit"
    ),
    path(
        "<int:pk>/delete/",
        CarRegistrationDeleteView.as_view(),
        name="registration_delete",
    ),
]
