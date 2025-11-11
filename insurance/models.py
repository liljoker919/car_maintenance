from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from vehicles.models import Vehicle


class InsurancePolicy(models.Model):
    """
    Insurance policy model for tracking vehicle insurance coverage.

    Tracks provider, policy number, coverage dates, and premium amounts.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Policy holder")
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="insurance_policies",
        help_text="Vehicle covered by this policy",
    )
    provider = models.CharField(max_length=100, help_text="Insurance provider name")
    policy_number = models.CharField(
        max_length=100, unique=True, help_text="Unique policy identification number"
    )
    coverage_start = models.DateField(help_text="Date coverage begins")
    coverage_end = models.DateField(help_text="Date coverage ends")
    premium = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Premium amount",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-coverage_end", "vehicle"]
        indexes = [
            models.Index(fields=["user", "-coverage_end"]),
            models.Index(fields=["vehicle", "-coverage_end"]),
            models.Index(fields=["coverage_end"]),
            models.Index(fields=["policy_number"]),
        ]
        verbose_name = "Insurance Policy"
        verbose_name_plural = "Insurance Policies"

    def __str__(self):
        return f"{self.provider} - {self.policy_number}"
