# Generated by Django 5.1 on 2024-09-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_alert_today'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='today',
            field=models.CharField(max_length=12),
        ),
    ]
