# Generated by Django 4.2.4 on 2023-08-06 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0003_alter_tag_type"),
        ("memes", "0001_initial"),
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
                ("meme_gif", models.URLField()),
                ("tags", models.ManyToManyField(related_name="tags", to="tags.tag")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="Memes",
        ),
    ]