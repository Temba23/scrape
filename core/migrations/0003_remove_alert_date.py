# Generated by Django 5.1 on 2024-08-17 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_alert_prev_alert_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='date',
        ),
    ]
