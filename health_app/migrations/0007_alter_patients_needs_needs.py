# Generated by Django 3.2.21 on 2024-03-03 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0006_alter_medicine_notification_medicine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients_needs',
            name='needs',
            field=models.CharField(max_length=100),
        ),
    ]
