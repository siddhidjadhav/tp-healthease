from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.contrib import messages
from datetime import datetime

def create_appointment(request):
    if request.method == 'POST':
        # Retrieve the appointment date and time from the form data
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        # Convert the date and time strings to datetime objects
        datetime_str = f'{date_str} {time_str}'
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        
        # Create a new appointment object
        appointment = Appointment(date=datetime_obj.date(), time=datetime_obj.time(), doctor=request.user)
        appointment.save()
        messages.success(request, 'Appointment created successfully!')
        return redirect('appointment_created')
    
