from django.db import models
from django.core.validators import MinValueValidator
from vehicles.models import Vehicle


class CarRegistration(models.Model):
    """
    Car registration model for tracking vehicle registration and inspection information.

    Tracks registration number, state, dates, and inspection schedules.
    """

    STATE_CHOICES = [
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
        ("DC", "District of Columbia"),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="car_registrations",
        help_text="Vehicle this registration applies to",
    )
    registration_number = models.CharField(
        max_length=50, help_text="Registration plate number"
    )
    state = models.CharField(
        max_length=2, choices=STATE_CHOICES, help_text="State of registration"
    )
    registration_date = models.DateField(help_text="Date registration was issued")
    expiration_date = models.DateField(help_text="Date registration expires")
    inspection_due_date = models.DateField(
        blank=True, null=True, help_text="Date inspection is due"
    )
    inspection_completed_date = models.DateField(
        blank=True, null=True, help_text="Date inspection was completed"
    )
    notes = models.TextField(blank=True, null=True, help_text="Additional notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-expiration_date", "vehicle"]
        indexes = [
            models.Index(fields=["vehicle", "-expiration_date"]),
            models.Index(fields=["expiration_date"]),
            models.Index(fields=["inspection_due_date"]),
        ]
        verbose_name = "Car Registration"
        verbose_name_plural = "Car Registrations"

    def __str__(self):
        return f"{self.vehicle} - {self.state} {self.registration_number}"
