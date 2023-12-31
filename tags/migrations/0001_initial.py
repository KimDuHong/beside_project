# Generated by Django 4.2.4 on 2023-08-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("상황", "상황"),
                            ("감정", "감정"),
                            ("인물", "인물"),
                            ("기타", "기타"),
                        ],
                        max_length=100,
                    ),
                ),
            ],
            options={
                "unique_together": {("name", "type")},
            },
        ),
    ]
