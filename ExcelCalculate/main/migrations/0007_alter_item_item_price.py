# Generated by Django 4.1.3 on 2022-11-21 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_item_item_img_alter_item_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_price',
            field=models.IntegerField(),
        ),
    ]