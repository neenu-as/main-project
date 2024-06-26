# Generated by Django 3.2.21 on 2024-03-16 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0009_alter_medicine_notification_medicine'),
    ]

    operations = [
        migrations.CreateModel(
            name='fall_detection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=40)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=100)),
                ('PATIENTID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.patient')),
            ],
        ),
    ]
