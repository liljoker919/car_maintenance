from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Vehicle
from .forms import VehicleForm
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = VehicleForm()
        return context


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = (
        "vehicles/vehicle_form.html"  # used for fallback if accessed directly
    )
    success_url = reverse_lazy("vehicle_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


from django.views.generic import DetailView


class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"
    context_object_name = "vehicle"

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)


from django.views.generic import UpdateView


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicle_list")

    def get_queryset(self):
        # Ensure users can only edit their own vehicles
        return Vehicle.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = "vehicles/vehicle_confirm_delete.html"
    success_url = reverse_lazy("vehicle_list")

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)


class VehicleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicle_list")
    success_message = "Vehicle deleted successfully."
    template_name = None  # prevent full-page rendering

    def get(self, request, *args, **kwargs):
        # Disable GET access to avoid showing full-page confirmation
        return redirect("vehicle_list")

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)
