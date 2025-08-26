from django import forms
from .models import Vehicle, ServiceRecord


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


class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = [
            "vehicle",
            "service_type",
            "date",
            "mileage",
            "cost",
            "notes",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Limit vehicle choices to current user's vehicles
            self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)
