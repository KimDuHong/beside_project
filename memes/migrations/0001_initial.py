# Generated by Django 4.2.4 on 2023-08-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tags", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Meme",
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
                ("title", models.CharField(max_length=100)),
                ("thumbnail", models.URLField(editable=False)),
                ("meme_url", models.URLField()),
                ("tags", models.ManyToManyField(related_name="tags", to="tags.tag")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
