# Generated by Django 5.1.5 on 2025-01-31 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_servicetype_alter_appointment_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='service_type',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='ServiceType',
        ),
    ]
