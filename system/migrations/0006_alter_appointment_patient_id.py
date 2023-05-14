# Generated by Django 4.1.7 on 2023-04-19 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0005_alter_appointment_patient_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL),
        ),
    ]