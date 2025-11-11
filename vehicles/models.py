from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Vehicle(models.Model):
    """
    Vehicle model representing a user's car or vehicle.

    Tracks basic vehicle information including make, model, year, mileage,
    VIN, condition, and optional nickname.
    """

    CONDITION_CHOICES = [
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vehicles",
        help_text="Owner of the vehicle",
    )
    make = models.CharField(max_length=50, help_text="Vehicle manufacturer")
    model = models.CharField(max_length=50, help_text="Vehicle model name")
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900, message="Year must be 1900 or later"),
            MaxValueValidator(
                datetime.now().year + 2,
                message=f"Year cannot be more than 1 year in the future",
            ),
        ],
        help_text="Manufacturing year",
    )
    current_mileage = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], help_text="Current odometer reading"
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        unique=True,
        help_text="Vehicle Identification Number (VIN) - must be unique",
    )
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default="good",
        help_text="Overall vehicle condition",
    )
    nickname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Optional friendly name for the vehicle",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "make", "model"]
        indexes = [
            models.Index(fields=["user", "-year"]),
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["vin"]),
        ]
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return (
            f"{self.year} {self.make} {self.model} ({self.nickname or 'No nickname'})"
        )


class ServiceRecord(models.Model):
    """
    Service record model for tracking vehicle maintenance and repairs.

    Records service type, date, mileage at service, cost, and additional notes.
    """

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

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="service_records",
        help_text="Vehicle this service was performed on",
    )
    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        help_text="Type of service performed",
    )
    date = models.DateField(help_text="Date service was performed")
    mileage = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Vehicle mileage at time of service",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Cost of service",
    )
    notes = models.TextField(
        blank=True, null=True, help_text="Additional notes about the service"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-mileage"]
        indexes = [
            models.Index(fields=["vehicle", "-date"]),
            models.Index(fields=["vehicle", "-mileage"]),
            models.Index(fields=["service_type", "-date"]),
        ]
        verbose_name = "Service Record"
        verbose_name_plural = "Service Records"

    def __str__(self):
        return f"{self.vehicle} - {self.get_service_type_display()} on {self.date}"
