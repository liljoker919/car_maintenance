# Generated migration to add indexes, validators, and help_text to Vehicle and ServiceRecord models

from datetime import datetime
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0002_servicerecord"),
    ]

    operations = [
        # Vehicle model updates
        migrations.AlterField(
            model_name="vehicle",
            name="user",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="vehicles",
                to="auth.user",
                help_text="Owner of the vehicle",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="make",
            field=models.CharField(max_length=50, help_text="Vehicle manufacturer"),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="model",
            field=models.CharField(max_length=50, help_text="Vehicle model name"),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="year",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1900, message="Year must be 1900 or later"
                    ),
                    django.core.validators.MaxValueValidator(
                        datetime.now().year + 2,
                        message=f"Year cannot be more than 1 year in the future",
                    ),
                ],
                help_text="Manufacturing year",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="current_mileage",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(0)],
                help_text="Current odometer reading",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="vin",
            field=models.CharField(
                max_length=17,
                blank=True,
                null=True,
                unique=True,
                help_text="Vehicle Identification Number (VIN) - must be unique",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="condition",
            field=models.CharField(
                max_length=10,
                choices=[
                    ("excellent", "Excellent"),
                    ("good", "Good"),
                    ("fair", "Fair"),
                    ("poor", "Poor"),
                ],
                default="good",
                help_text="Overall vehicle condition",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="nickname",
            field=models.CharField(
                max_length=50,
                blank=True,
                null=True,
                help_text="Optional friendly name for the vehicle",
            ),
        ),
        # Add Vehicle indexes
        migrations.AddIndex(
            model_name="vehicle",
            index=models.Index(
                fields=["user", "-year"], name="vehicles_v_user_id_1a2b3c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="vehicle",
            index=models.Index(
                fields=["user", "created_at"], name="vehicles_v_user_id_4d5e6f_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="vehicle",
            index=models.Index(fields=["vin"], name="vehicles_v_vin_7g8h9i_idx"),
        ),
        # Add Vehicle meta options
        migrations.AlterModelOptions(
            name="vehicle",
            options={
                "ordering": ["-year", "make", "model"],
                "verbose_name": "Vehicle",
                "verbose_name_plural": "Vehicles",
            },
        ),
        # ServiceRecord model updates
        migrations.AlterField(
            model_name="servicerecord",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="service_records",
                to="vehicles.vehicle",
                help_text="Vehicle this service was performed on",
            ),
        ),
        migrations.AlterField(
            model_name="servicerecord",
            name="service_type",
            field=models.CharField(
                max_length=50,
                choices=[
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
                ],
                help_text="Type of service performed",
            ),
        ),
        migrations.AlterField(
            model_name="servicerecord",
            name="date",
            field=models.DateField(help_text="Date service was performed"),
        ),
        migrations.AlterField(
            model_name="servicerecord",
            name="mileage",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(0)],
                help_text="Vehicle mileage at time of service",
            ),
        ),
        migrations.AlterField(
            model_name="servicerecord",
            name="cost",
            field=models.DecimalField(
                max_digits=10,
                decimal_places=2,
                validators=[django.core.validators.MinValueValidator(0)],
                help_text="Cost of service",
            ),
        ),
        migrations.AlterField(
            model_name="servicerecord",
            name="notes",
            field=models.TextField(
                blank=True, null=True, help_text="Additional notes about the service"
            ),
        ),
        # Add ServiceRecord indexes
        migrations.AddIndex(
            model_name="servicerecord",
            index=models.Index(
                fields=["vehicle", "-date"], name="vehicles_s_vehicle_1j2k3l_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="servicerecord",
            index=models.Index(
                fields=["vehicle", "-mileage"], name="vehicles_s_vehicle_4m5n6o_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="servicerecord",
            index=models.Index(
                fields=["service_type", "-date"], name="vehicles_s_service_7p8q9r_idx"
            ),
        ),
        # Add ServiceRecord meta options
        migrations.AlterModelOptions(
            name="servicerecord",
            options={
                "ordering": ["-date", "-mileage"],
                "verbose_name": "Service Record",
                "verbose_name_plural": "Service Records",
            },
        ),
    ]
