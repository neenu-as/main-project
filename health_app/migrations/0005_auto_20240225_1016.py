# Generated by Django 3.2.21 on 2024-02-25 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0004_alter_patient_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine_notification',
            name='CAMERAID',
        ),
        migrations.AddField(
            model_name='medicine_notification',
            name='CARETAKERID',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='health_app.caretaker'),
            preserve_default=False,
        ),
    ]
