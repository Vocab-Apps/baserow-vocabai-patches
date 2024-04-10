# Generated by Django 4.0.10 on 2024-01-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0148_add_formula_button_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="durationfield",
            name="duration_format",
            field=models.CharField(
                choices=[
                    ("h:mm", "hours:minutes"),
                    ("h:mm:ss", "hours:minutes:seconds"),
                    ("h:mm:ss.s", "hours:minutes:seconds:deciseconds"),
                    ("h:mm:ss.ss", "hours:minutes:seconds:centiseconds"),
                    ("h:mm:ss.sss", "hours:minutes:seconds:milliseconds"),
                    ("d h", "days:hours"),
                    ("d h:mm", "days:hours:minutes"),
                    ("d h:mm:ss", "days:hours:minutes:seconds"),
                ],
                default="h:mm",
                help_text="The format of the duration.",
                max_length=32,
            ),
        ),
    ]