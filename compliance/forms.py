from django import forms
from .models import CarRegistration


class CarRegistrationForm(forms.ModelForm):
    class Meta:
        model = CarRegistration
        fields = [
            "vehicle",
            "registration_number",
            "state",
            "registration_date",
            "expiration_date",
            "inspection_due_date",
            "inspection_completed_date",
            "notes",
        ]
        widgets = {
            "registration_date": forms.DateInput(attrs={"type": "date"}),
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
            "inspection_due_date": forms.DateInput(attrs={"type": "date"}),
            "inspection_completed_date": forms.DateInput(attrs={"type": "date"}),
            "state": forms.Select(attrs={"class": "form-select"}),
            "vehicle": forms.Select(attrs={"class": "form-select"}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
