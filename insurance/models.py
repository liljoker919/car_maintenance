from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle  # assumes vehicles app exists


class InsurancePolicy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="insurance_policies"
    )
    provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100, unique=True)
    coverage_start = models.DateField()
    coverage_end = models.DateField()
    premium = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.provider} - {self.policy_number}"
