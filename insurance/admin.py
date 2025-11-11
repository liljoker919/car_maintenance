from django.contrib import admin
from .models import InsurancePolicy


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    """Enhanced admin interface for InsurancePolicy model."""

    list_display = [
        "vehicle",
        "provider",
        "policy_number",
        "coverage_start",
        "coverage_end",
        "premium",
        "user",
        "created_at",
    ]
    list_filter = ["provider", "coverage_end", "user"]
    search_fields = [
        "policy_number",
        "provider",
        "vehicle__make",
        "vehicle__model",
        "user__username",
    ]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "coverage_end"
    ordering = ["-coverage_end"]

    fieldsets = (
        ("Policy Holder", {"fields": ("user", "vehicle")}),
        ("Policy Details", {"fields": ("provider", "policy_number", "premium")}),
        ("Coverage Period", {"fields": ("coverage_start", "coverage_end")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
