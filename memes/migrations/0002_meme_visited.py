# Generated by Django 4.2.4 on 2023-08-09 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("memes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="meme",
            name="visited",
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
