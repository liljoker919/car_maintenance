from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from vehicles.models import Vehicle
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

    def form_invalid(self, form):
        # Store form errors in session and redirect back to vehicle detail page
        vehicle_id = self.request.POST.get('vehicle')
        if vehicle_id:
            try:
                vehicle = get_object_or_404(Vehicle, id=vehicle_id, user=self.request.user)
                # Store form data and errors in session
                self.request.session['registration_form_errors'] = form.errors.as_json()
                self.request.session['registration_form_data'] = self.request.POST.dict()
                messages.error(self.request, 'Please correct the errors below.')
                return redirect('vehicles:vehicle_detail', pk=vehicle.pk)
            except (Vehicle.DoesNotExist, ValueError):
                pass
        # Fallback to default behavior if we can't determine the vehicle
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk})


class CarRegistrationUpdateView(LoginRequiredMixin, UpdateView):
    model = CarRegistration
    form_class = CarRegistrationForm
    template_name = "compliance/registration_form.html"

    def get_queryset(self):
        # Only allow editing registrations for vehicles owned by the current user
        return CarRegistration.objects.filter(vehicle__user=self.request.user)

    def form_invalid(self, form):
        # Store form errors in session and redirect back to vehicle detail page
        if self.object and self.object.vehicle:
            # Store form data and errors in session
            self.request.session['registration_edit_form_errors'] = form.errors.as_json()
            self.request.session['registration_edit_form_data'] = self.request.POST.dict()
            self.request.session['registration_edit_form_id'] = self.object.id
            messages.error(self.request, 'Please correct the errors below.')
            return redirect('vehicles:vehicle_detail', pk=self.object.vehicle.pk)
        # Fallback to default behavior
        return super().form_invalid(form)

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
