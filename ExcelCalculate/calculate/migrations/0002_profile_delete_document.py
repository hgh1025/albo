# Generated by Django 4.1.1 on 2022-11-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculate", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("title", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.DeleteModel(name="Document",),
    ]
