from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    CONDITION_CHOICES = [
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    current_mileage = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, blank=True, null=True)
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default="good"
    )
    nickname = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "make", "model"]

    def __str__(self):
        return (
            f"{self.year} {self.make} {self.model} ({self.nickname or 'No nickname'})"
        )


class ServiceRecord(models.Model):
    SERVICE_TYPE_CHOICES = [
        ("oil_change", "Oil Change"),
        ("tire_rotation", "Tire Rotation"),
        ("brake_service", "Brake Service"),
        ("transmission_service", "Transmission Service"),
        ("air_filter", "Air Filter Replacement"),
        ("cabin_filter", "Cabin Filter Replacement"),
        ("tune_up", "Tune Up"),
        ("inspection", "Inspection"),
        ("repair", "Repair"),
        ("other", "Other"),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="service_records")
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    date = models.DateField()
    mileage = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-mileage"]

    def __str__(self):
        return f"{self.vehicle} - {self.get_service_type_display()} on {self.date}"
