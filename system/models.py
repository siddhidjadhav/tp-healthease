from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Appointment(models.Model):
    patient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient", null=True, blank=True)
    doctor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, default='open', blank=True)
    prescription = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Appointment is on {self.date}"
