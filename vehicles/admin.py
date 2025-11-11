from django.contrib import admin
from .models import Vehicle, ServiceRecord


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Vehicle model."""

    list_display = [
        "year",
        "make",
        "model",
        "nickname",
        "user",
        "current_mileage",
        "condition",
        "vin",
        "created_at",
    ]
    list_filter = ["condition", "year", "make", "user"]
    search_fields = ["make", "model", "vin", "nickname", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
    ordering = ["-year", "make", "model"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("user", "make", "model", "year", "nickname")},
        ),
        ("Details", {"fields": ("vin", "current_mileage", "condition")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    """Enhanced admin interface for ServiceRecord model."""

    list_display = ["vehicle", "service_type", "date", "mileage", "cost", "created_at"]
    list_filter = ["service_type", "date", "vehicle__make", "vehicle__user"]
    search_fields = ["vehicle__make", "vehicle__model", "notes"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "date"
    ordering = ["-date", "-mileage"]

    fieldsets = (
        (
            "Service Information",
            {"fields": ("vehicle", "service_type", "date", "mileage", "cost")},
        ),
        ("Additional Details", {"fields": ("notes",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
