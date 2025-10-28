import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InsurancePolicy
from .forms import InsurancePolicyForm  # Correct form name

logger = logging.getLogger(__name__)


class InsuranceCreateView(LoginRequiredMixin, CreateView):
    model = InsurancePolicy
    form_class = InsurancePolicyForm
    template_name = "insurance_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        logger.info("User %s created insurance policy for vehicle: %s", self.request.user.username, form.instance.vehicle)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk})


class InsuranceUpdateView(LoginRequiredMixin, UpdateView):
    model = InsurancePolicy
    form_class = InsurancePolicyForm
    template_name = "insurance_form.html"

    def form_valid(self, form):
        logger.info("User %s updated insurance policy for vehicle: %s", self.request.user.username, form.instance.vehicle)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk})


class InsuranceDeleteView(LoginRequiredMixin, DeleteView):
    model = InsurancePolicy
    template_name = "insurance_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        policy = self.get_object()
        logger.info("User %s deleted insurance policy for vehicle: %s", request.user.username, policy.vehicle)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("vehicles:vehicle_detail", kwargs={"pk": self.object.vehicle.pk})
