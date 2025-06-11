from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Vehicle
from .forms import VehicleForm
from insurance.models import InsurancePolicy
from insurance.forms import InsurancePolicyForm


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)


class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"
    context_object_name = "vehicle"

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["insurance_policies"] = InsurancePolicy.objects.filter(
            vehicle=self.object, user=self.request.user
        )
        context["insurance_form"] = InsurancePolicyForm(
            initial={"vehicle": self.object}
        )
        return context


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicle_list")


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("vehicle_list")


class VehicleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicle_list")
    success_message = "Vehicle deleted successfully."
    template_name = None  # handled via modal, no confirmation page

    def get(self, request, *args, **kwargs):
        return redirect("vehicle_list")  # disable GET access

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)
