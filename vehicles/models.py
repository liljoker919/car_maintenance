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


class Insurance(models.Model):
    provider = models.CharField(max_length=100)
    renewal_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    policy_number = models.CharField(max_length=50)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="insurances")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-renewal_date"]

    def __str__(self):
        return f"{self.provider} - {self.policy_number} ({self.vehicle})"
