# Generated migration to add timestamps and indexes to InsurancePolicy

from django.db import migrations, models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("insurance", "0001_initial"),
    ]

    operations = [
        # Add created_at field
        migrations.AddField(
            model_name="insurancepolicy",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        # Add updated_at field
        migrations.AddField(
            model_name="insurancepolicy",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        # Update provider field with help_text
        migrations.AlterField(
            model_name="insurancepolicy",
            name="provider",
            field=models.CharField(
                max_length=100, help_text="Insurance provider name"
            ),
        ),
        # Update policy_number field with help_text
        migrations.AlterField(
            model_name="insurancepolicy",
            name="policy_number",
            field=models.CharField(
                max_length=100,
                unique=True,
                help_text="Unique policy identification number",
            ),
        ),
        # Update coverage_start field with help_text
        migrations.AlterField(
            model_name="insurancepolicy",
            name="coverage_start",
            field=models.DateField(help_text="Date coverage begins"),
        ),
        # Update coverage_end field with help_text
        migrations.AlterField(
            model_name="insurancepolicy",
            name="coverage_end",
            field=models.DateField(help_text="Date coverage ends"),
        ),
        # Update premium field with validators and help_text
        migrations.AlterField(
            model_name="insurancepolicy",
            name="premium",
            field=models.DecimalField(
                max_digits=10,
                decimal_places=2,
                validators=[django.core.validators.MinValueValidator(0)],
                help_text="Premium amount",
            ),
        ),
        # Update user field with help_text
        migrations.AlterField(
            model_name="insurancepolicy",
            name="user",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                to="auth.user",
                help_text="Policy holder",
            ),
        ),
        # Update vehicle field with help_text
        migrations.AlterField(
            model_name="insurancepolicy",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="insurance_policies",
                to="vehicles.vehicle",
                help_text="Vehicle covered by this policy",
            ),
        ),
        # Add model meta options
        migrations.AlterModelOptions(
            name="insurancepolicy",
            options={
                "ordering": ["-coverage_end", "vehicle"],
                "verbose_name": "Insurance Policy",
                "verbose_name_plural": "Insurance Policies",
            },
        ),
        # Add indexes
        migrations.AddIndex(
            model_name="insurancepolicy",
            index=models.Index(
                fields=["user", "-coverage_end"], name="insurance_i_user_id_8a7c6b_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="insurancepolicy",
            index=models.Index(
                fields=["vehicle", "-coverage_end"],
                name="insurance_i_vehicle_9d4e5f_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="insurancepolicy",
            index=models.Index(
                fields=["coverage_end"], name="insurance_i_coverag_1a2b3c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="insurancepolicy",
            index=models.Index(
                fields=["policy_number"], name="insurance_i_policy__4d5e6f_idx"
            ),
        ),
    ]
