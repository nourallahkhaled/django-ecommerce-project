# Generated by Django 4.2.2 on 2023-06-24 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wearstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]