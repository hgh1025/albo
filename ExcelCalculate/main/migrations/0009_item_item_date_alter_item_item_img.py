# Generated by Django 4.1.3 on 2022-11-24 05:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_item_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='item_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
