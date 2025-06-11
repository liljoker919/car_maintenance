from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InsurancePolicy
from .forms import InsurancePolicyForm  # Correct form name


class InsuranceCreateView(CreateView):
    model = InsurancePolicy
    form_class = InsurancePolicyForm
    template_name = "insurance_form.html"

    def form_valid(self, form):
        vehicle_id = self.kwargs.get("vehicle_pk")
        form.instance.vehicle_id = vehicle_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("vehicle_detail", kwargs={"pk": self.object.vehicle.pk})


class InsuranceUpdateView(UpdateView):
    model = InsurancePolicy
    form_class = InsurancePolicyForm
    template_name = "insurance_form.html"

    def get_success_url(self):
        return reverse_lazy("vehicle_detail", kwargs={"pk": self.object.vehicle.pk})


class InsuranceDeleteView(DeleteView):
    model = InsurancePolicy
    template_name = "insurance_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("vehicle_detail", kwargs={"pk": self.object.vehicle.pk})
