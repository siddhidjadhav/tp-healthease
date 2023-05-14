from django.shortcuts import render, redirect
import re
from .utility import check_if_user_is_doctor
from django.contrib.auth import get_user_model
from system.models import Appointment
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def doctor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    user_status = check_if_user_is_doctor(request.user)
    if not user_status["is_user_doctor"]:
        return redirect(user_status["user_identity"]) 
    # if not re.match(".@healthease.com$", user_email):
    #     message = "yes match"
    #     if re.search(".@gmail.com$", user_email):
    #         message = "yes"
    #         return redirect('patient_dashboard')

    if request.method=='POST':
        appointment_id = request.POST.get('appointment_id')
        return redirect(f'add_prescription/{appointment_id}',)


    todays_date = timezone.now().date()
    current_time = timezone.now()
    appointment_for_today = Appointment.objects.filter(date=todays_date, doctor_id=request.user, patient_id__isnull=False).exclude(status='closed')
    upcoming_appointments = Appointment.objects.filter(doctor_id=request.user).exclude(date=todays_date)
    booked_appointments = 0
    not_booked_appointments = 0
    total_appointments = Appointment.objects.filter(date=todays_date, doctor_id=request.user).exclude(status='closed')
    for appointment in total_appointments:
        if appointment.patient_id:
            booked_appointments = booked_appointments+1
        else:
            not_booked_appointments = not_booked_appointments+1

    doctor = f"{request.user.first_name} {request.user.last_name}"
    return render(request, 'doctor_dashboard.html', { 'doctor':doctor, 'appointment_for_today':appointment_for_today, 'booked': booked_appointments, 'not_booked': not_booked_appointments, 'total_appointments': total_appointments.count(), 'request': request, 'todays_date': todays_date})


def create_appointment(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        if appointment_id is not None:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.delete()
            return redirect('create_appointment')

    if request.method == 'POST':
        # Retrieve the appointment date and time from the form data
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        # Convert the date and time strings to datetime objects
        datetime_str = f'{date_str} {time_str}'
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        
        # Create a new appointment object
        appointment = Appointment(date=datetime_obj.date(), time=datetime_obj.time(), doctor_id=request.user)
        appointment.save()
        return redirect('create_appointment')
    
    else:
        appointments = Appointment.objects.filter(doctor_id=request.user)
        return render(request, 'create_appointment.html', {'appointments': appointments, 'request': request})
    

def add_prescription(request, appointment_id):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    if request.method=="POST":
        status = request.POST.get('status')
        prescription = request.POST.get('prescription')

        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = status 
        appointment.prescription = prescription
        appointment.save()

        return redirect('doctor_dashboard')
    
    appointment = Appointment.objects.get(id=appointment_id)
    patient = get_user_model().objects.get(id=appointment.patient_id.id)
    appointment_history = Appointment.objects.filter(patient_id=patient, status='closed')

    return render(request, 'add_prescription.html', {'appointment': appointment, 'appointment_history': appointment_history, 'patient': patient, 'request': request})
    
def appointments_list(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    appointment_list = Appointment.objects.filter(doctor_id=request.user).order_by('date', 'time')
    paginator = Paginator(appointment_list, 10) # Show 10 appointments per page

    page = request.GET.get('page')
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        appointments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        appointments = paginator.page(paginator.num_pages)

    return render(request, 'all_appointments.html', {'appointments': appointments, 'request': request})