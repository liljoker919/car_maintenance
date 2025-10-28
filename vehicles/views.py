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
from .models import Vehicle, ServiceRecord
from .forms import VehicleForm, ServiceRecordForm
from insurance.models import InsurancePolicy
from insurance.forms import InsurancePolicyForm
from compliance.models import CarRegistration
from compliance.forms import CarRegistrationForm


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


class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"
    context_object_name = "vehicle"

    def get_queryset(self):
        # Fetch the vehicle and prefetch all related lists efficiently
        return Vehicle.objects.filter(user=self.request.user).prefetch_related(
            "insurance_policies", "car_registrations", "service_records"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use prefetched data instead of separate queries
        context["insurance_policies"] = self.object.insurance_policies.all()
        context["insurance_form"] = InsurancePolicyForm(
            initial={"vehicle": self.object}
        )
        # Add registration-related context (uses prefetched data)
        context["car_registrations"] = self.object.car_registrations.all()

        # Add service records context (uses prefetched data)
        context["service_records"] = self.object.service_records.all()

        # Check for service record form errors in session
        service_form_errors = self.request.session.pop("service_form_errors", None)
        service_form_data = self.request.session.pop("service_form_data", None)

        if service_form_errors and service_form_data:
            # Recreate form with errors and data for the add modal
            import json
            from django.forms.utils import ErrorDict

            service_form = ServiceRecordForm(
                data=service_form_data, user=self.request.user
            )
            service_form._errors = ErrorDict(json.loads(service_form_errors))
            context["service_form"] = service_form
        else:
            context["service_form"] = ServiceRecordForm(
                initial={"vehicle": self.object}, user=self.request.user
            )

        # Check for service record edit form errors in session
        service_edit_form_errors = self.request.session.pop(
            "service_edit_form_errors", None
        )
        service_edit_form_data = self.request.session.pop(
            "service_edit_form_data", None
        )
        service_edit_form_id = self.request.session.pop("service_edit_form_id", None)

        if service_edit_form_errors and service_edit_form_data and service_edit_form_id:
            context["service_edit_form_errors"] = service_edit_form_errors
            context["service_edit_form_data"] = service_edit_form_data
            context["service_edit_form_id"] = service_edit_form_id

        # Check for registration form errors in session
        registration_form_errors = self.request.session.pop(
            "registration_form_errors", None
        )
        registration_form_data = self.request.session.pop(
            "registration_form_data", None
        )

        if registration_form_errors and registration_form_data:
            # Recreate form with errors and data for the add modal
            import json
            from django.forms.utils import ErrorDict
            from django.utils.safestring import mark_safe

            registration_form = CarRegistrationForm(
                data=registration_form_data, initial={"vehicle": self.object}
            )
            # Manually add the errors to the form
            registration_form._errors = ErrorDict(json.loads(registration_form_errors))
            context["registration_form"] = registration_form
        else:
            context["registration_form"] = CarRegistrationForm(
                initial={"vehicle": self.object}
            )

        # Check for edit form errors in session
        registration_edit_form_errors = self.request.session.pop(
            "registration_edit_form_errors", None
        )
        registration_edit_form_data = self.request.session.pop(
            "registration_edit_form_data", None
        )
        registration_edit_form_id = self.request.session.pop(
            "registration_edit_form_id", None
        )

        if (
            registration_edit_form_errors
            and registration_edit_form_data
            and registration_edit_form_id
        ):
            # Store edit form errors to be displayed in the specific edit modal
            context["registration_edit_form_errors"] = registration_edit_form_errors
            context["registration_edit_form_data"] = registration_edit_form_data
            context["registration_edit_form_id"] = registration_edit_form_id

        # Add form for editing the vehicle
        context["form"] = VehicleForm(instance=self.object)
        return context


class VehicleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = None  # Using modal, no template needed
    success_message = "Vehicle created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_list")

    def get(self, request, *args, **kwargs):
        # For GET requests, redirect to vehicle list since we're using modals
        return redirect("vehicles:vehicle_list")


class VehicleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = None  # Using modal, no template needed
    success_message = "Vehicle updated successfully."

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def get_success_url(self):
        # Check if request came from detail page or list page
        referer = self.request.META.get("HTTP_REFERER", "")
        if "detail" in referer:
            return reverse_lazy(
                "vehicles:vehicle_detail", kwargs={"pk": self.object.pk}
            )
        return reverse_lazy("vehicles:vehicle_list")

    def get(self, request, *args, **kwargs):
        # For GET requests, redirect to the appropriate page since we're using modals
        referer = request.META.get("HTTP_REFERER", "")
        if "detail" in referer:
            return redirect("vehicles:vehicle_detail", pk=kwargs["pk"])
        return redirect("vehicles:vehicle_list")


class VehicleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicles:vehicle_list")
    success_message = "Vehicle deleted successfully."
    template_name = None  # handled via modal, no confirmation page

    def get(self, request, *args, **kwargs):
        return redirect("vehicles:vehicle_list")  # disable GET access

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)


# ServiceRecord CRUD Views
class ServiceRecordCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ServiceRecord
    form_class = ServiceRecordForm
    template_name = None  # Using modal, no template needed
    success_message = "Service record created successfully."

    def form_valid(self, form):
        # Ensure the service record belongs to a vehicle owned by the user
        if form.instance.vehicle.user != self.request.user:
            return redirect("vehicles:vehicle_list")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Store form errors and data in session for modal display
        import json

        self.request.session["service_form_errors"] = json.dumps(dict(form.errors))
        self.request.session["service_form_data"] = form.data

        # Redirect back to vehicle detail page
        vehicle_id = form.data.get("vehicle")
        if vehicle_id:
            return redirect("vehicles:vehicle_detail", pk=vehicle_id)
        return redirect("vehicles:vehicle_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy(
            "vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk}
        )

    def get(self, request, *args, **kwargs):
        # For GET requests, redirect to vehicle list since we're using modals
        return redirect("vehicles:vehicle_list")


class ServiceRecordUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ServiceRecord
    form_class = ServiceRecordForm
    template_name = None  # Using modal, no template needed
    success_message = "Service record updated successfully."

    def get_queryset(self):
        # Only allow editing service records for vehicles owned by the user
        return ServiceRecord.objects.filter(vehicle__user=self.request.user)

    def form_invalid(self, form):
        # Store form errors and data in session for modal display
        import json

        self.request.session["service_edit_form_errors"] = json.dumps(dict(form.errors))
        self.request.session["service_edit_form_data"] = form.data
        self.request.session["service_edit_form_id"] = self.object.id

        # Redirect back to vehicle detail page
        return redirect("vehicles:vehicle_detail", pk=self.object.vehicle.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy(
            "vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk}
        )

    def get(self, request, *args, **kwargs):
        # For GET requests, redirect to vehicle detail page
        return redirect("vehicles:vehicle_detail", pk=self.get_object().vehicle.pk)


class ServiceRecordDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ServiceRecord
    success_message = "Service record deleted successfully."
    template_name = None  # handled via modal, no confirmation page

    def get_queryset(self):
        # Only allow deleting service records for vehicles owned by the user
        return ServiceRecord.objects.filter(vehicle__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk}
        )

    def get(self, request, *args, **kwargs):
        # For GET requests, redirect to vehicle detail page
        return redirect("vehicles:vehicle_detail", pk=self.get_object().vehicle.pk)
