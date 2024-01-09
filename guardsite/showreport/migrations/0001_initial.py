# Generated by Django 4.2 on 2024-01-08 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Checklist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("context", models.TextField()),
            ],
            options={
                "db_table": "checklist",
            },
        ),
        migrations.CreateModel(
            name="ChecklistEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_at", models.DateField()),
                ("truefalse", models.BooleanField()),
                (
                    "context",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="showreport.checklist",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "report",
            },
        ),
    ]
