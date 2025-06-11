from django.urls import path
from .views import InsuranceCreateView, InsuranceUpdateView, InsuranceDeleteView

urlpatterns = [
    path("add/", InsuranceCreateView.as_view(), name="insurance_add"),
    path("<int:pk>/edit/", InsuranceUpdateView.as_view(), name="insurance_edit"),
    path("<int:pk>/delete/", InsuranceDeleteView.as_view(), name="insurance_delete"),
]
