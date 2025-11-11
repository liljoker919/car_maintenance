from django.contrib import admin
from .models import CarRegistration


@admin.register(CarRegistration)
class CarRegistrationAdmin(admin.ModelAdmin):
    """Enhanced admin interface for CarRegistration model."""

    list_display = [
        "vehicle",
        "registration_number",
        "state",
        "registration_date",
        "expiration_date",
        "inspection_due_date",
        "created_at",
    ]
    list_filter = ["state", "expiration_date", "inspection_due_date"]
    search_fields = ["registration_number", "vehicle__make", "vehicle__model", "state"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "expiration_date"
    ordering = ["-expiration_date"]

    fieldsets = (
        ("Vehicle Information", {"fields": ("vehicle",)}),
        (
            "Registration Details",
            {
                "fields": (
                    "registration_number",
                    "state",
                    "registration_date",
                    "expiration_date",
                )
            },
        ),
        (
            "Inspection Information",
            {"fields": ("inspection_due_date", "inspection_completed_date")},
        ),
        ("Additional Information", {"fields": ("notes",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
