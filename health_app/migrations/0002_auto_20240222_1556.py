# Generated by Django 3.2.21 on 2024-02-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login_table',
            name='password',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='pillreminder',
            name='time',
            field=models.CharField(max_length=40),
        ),
    ]