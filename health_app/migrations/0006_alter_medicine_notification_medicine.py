# Generated by Django 3.2.21 on 2024-02-25 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0005_auto_20240225_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine_notification',
            name='medicine',
            field=models.CharField(max_length=100),
        ),
    ]
