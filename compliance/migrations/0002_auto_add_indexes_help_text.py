# Generated migration to add indexes and help_text to CarRegistration model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compliance", "0001_initial"),
    ]

    operations = [
        # Update vehicle field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="car_registrations",
                to="vehicles.vehicle",
                help_text="Vehicle this registration applies to",
            ),
        ),
        # Update registration_number field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="registration_number",
            field=models.CharField(
                max_length=50, help_text="Registration plate number"
            ),
        ),
        # Update state field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="state",
            field=models.CharField(
                max_length=2,
                choices=[
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
                ],
                help_text="State of registration",
            ),
        ),
        # Update registration_date field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="registration_date",
            field=models.DateField(help_text="Date registration was issued"),
        ),
        # Update expiration_date field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="expiration_date",
            field=models.DateField(help_text="Date registration expires"),
        ),
        # Update inspection_due_date field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="inspection_due_date",
            field=models.DateField(
                blank=True, null=True, help_text="Date inspection is due"
            ),
        ),
        # Update inspection_completed_date field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="inspection_completed_date",
            field=models.DateField(
                blank=True, null=True, help_text="Date inspection was completed"
            ),
        ),
        # Update notes field with help_text
        migrations.AlterField(
            model_name="carregistration",
            name="notes",
            field=models.TextField(blank=True, null=True, help_text="Additional notes"),
        ),
        # Add model meta options
        migrations.AlterModelOptions(
            name="carregistration",
            options={
                "ordering": ["-expiration_date", "vehicle"],
                "verbose_name": "Car Registration",
                "verbose_name_plural": "Car Registrations",
            },
        ),
        # Add indexes
        migrations.AddIndex(
            model_name="carregistration",
            index=models.Index(
                fields=["vehicle", "-expiration_date"],
                name="compliance_vehicle_1s2t3u_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="carregistration",
            index=models.Index(
                fields=["expiration_date"], name="compliance_expirat_4v5w6x_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="carregistration",
            index=models.Index(
                fields=["inspection_due_date"], name="compliance_inspect_7y8z9a_idx"
            ),
        ),
    ]
