from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "make",
            "model",
            "year",
            "current_mileage",
            "vin",
            "condition",
            "nickname",
        ]
