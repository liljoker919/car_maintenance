from django import forms
from .models import InsurancePolicy


class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = [
            "vehicle",
            "provider",
            "policy_number",
            "coverage_start",
            "coverage_end",
            "premium",
        ]
        widgets = {
            "coverage_start": forms.DateInput(attrs={"type": "date"}),
            "coverage_end": forms.DateInput(attrs={"type": "date"}),
        }
