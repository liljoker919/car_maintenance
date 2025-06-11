from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CarRegistration
from .forms import CarRegistrationForm


class CarRegistrationCreateView(LoginRequiredMixin, CreateView):
    model = CarRegistration
    form_class = CarRegistrationForm
    template_name = "compliance/registration_form.html"

    def form_valid(self, form):
        # Ensure the vehicle belongs to the current user
        vehicle = form.cleaned_data['vehicle']
        if vehicle.user != self.request.user:
            form.add_error('vehicle', 'You can only add registrations to your own vehicles.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk})


class CarRegistrationUpdateView(LoginRequiredMixin, UpdateView):
    model = CarRegistration
    form_class = CarRegistrationForm
    template_name = "compliance/registration_form.html"

    def get_queryset(self):
        # Only allow editing registrations for vehicles owned by the current user
        return CarRegistration.objects.filter(vehicle__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk})


class CarRegistrationDeleteView(LoginRequiredMixin, DeleteView):
    model = CarRegistration
    template_name = "compliance/registration_confirm_delete.html"

    def get_queryset(self):
        # Only allow deleting registrations for vehicles owned by the current user
        return CarRegistration.objects.filter(vehicle__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk})
