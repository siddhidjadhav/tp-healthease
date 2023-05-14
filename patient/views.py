from django.shortcuts import render, redirect
from datetime import date, timedelta
from .utility import check_if_user_is_patient
from django.contrib.auth import get_user_model
from system.models import Appointment
from insurance_provider.models import InsuranceDetails, InsurancePurchaseHistory
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from django.db.models import Q

def patient_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    user_status = check_if_user_is_patient(request.user)
    if not user_status["is_user_patient"]:
        return redirect(user_status["user_identity"])
    
    
    query = ""
    doctors = get_user_model().objects.filter(email__contains='@healthease.com')
    if request.method == 'POST':
        query = request.POST.get('q')
        doctor_id = request.POST.get('doctor_id')
        clear = request.POST.get('clear')

        if doctor_id:
            return redirect(f'book_appointment/{doctor_id}',)

        if query:
        # use Q objects to search first and last name
            doctors = doctors.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            

    appointments = Appointment.objects.filter(patient_id=request.user, status='booked')
    total_appointments = len(appointments)
    purchased_insurances = InsurancePurchaseHistory.objects.filter(customer=request.user)
    return render(request, 'patient_dashboard.html', {'doctors': doctors, 'appointments': appointments, 'total_appointments': total_appointments, 'purchased_insurances': len(purchased_insurances), 'query': query})

def doctor_details(request):
    doctor = {
        'name' : 'Manoj Kataria',
        'email' : 'manoj@gmail.com',
        'specialization' : 'MD, PHD',
        'address': 'Manas Hospital, Bharati Vidyapeth'
    }

    max_date = (date.today() + timedelta(days=6)).strftime("%Y-%m-%d")
    min_date = date.today().strftime("%Y-%m-%d")
    return render(request, 'doctor_info.html', {'doctor': doctor, 'min_date': min_date, 'max_date': max_date})

def patient_appointment(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        
        # Check if the appointment id is valid
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            appointment = None
        
        if appointment is not None:
            # If the appointment id is valid, assign the appointment to the current user
            appointment.patient_id = None
            appointment.status = 'open'
            appointment.save()
            email_content = '<p>Hello ' + request.user.first_name + ',</p><p><strong>Your Appointment with Dr.' + appointment.doctor_id.first_name + ' on ' + appointment.date.strftime("%Y-%m-%d") + ' at ' + appointment.time.strftime("%H:%M:%S") + ' is cancelled.</strong></p><p>Thank you,<br>HealthEase</p>'
            message = Mail(
                    from_email='patilom2114@gmail.com',
                    to_emails= request.user.email,
                    subject='Appointment Cancelled',
                    html_content=email_content
                )
            try:
                sg = SendGridAPIClient(api_key='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')
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(str(e))
            return redirect('patient_appointment')
        
    appointments = Appointment.objects.filter(patient_id = request.user).exclude(status='closed')
    return render(request, 'appointment.html', {'appointments': appointments})


def book_appointment(request, doctor_id):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    if request.method == 'POST':
        # Retrieve the selected date and appointment id from the form data
        selected_date_str = request.POST.get('selected_date')
        appointment_id = request.POST.get('appointment_id')
        
        # Check if the appointment id is valid
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            appointment = None
        
        if appointment is not None:
            # If the appointment id is valid, assign the appointment to the current user
            appointment.patient_id = request.user
            appointment.status = 'booked'
            appointment.save()
            email_content = '<p>Hello ' + request.user.first_name + ',</p><p><strong>Your Appointment with Dr.' + appointment.doctor_id.first_name + ' is confirmed on ' + appointment.date.strftime("%Y-%m-%d") + ' at ' + appointment.time.strftime("%H:%M:%S") + '.</strong></p><p>Thank you,<br>HealthEase</p>'
            message = Mail(
                    from_email='patilom2114@gmail.com',
                    to_emails= request.user.email,
                    subject='Appointment Confirmation',
                    html_content=email_content
                )
            try:
                sg = SendGridAPIClient(api_key='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')
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(str(e))
            return redirect('patient_appointment')
        
    # If the request method is GET or the appointment id is not valid, display the calendar and appointments for the selected date
    if request.method == 'POST':
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()
    
    doctor = get_object_or_404(User, id=doctor_id)
    appointments = Appointment.objects.filter(doctor_id=doctor, date=selected_date, patient_id=None)
    doctors_appointment_history = Appointment.objects.filter(doctor_id=doctor).exclude(patient_id=None)
    unique_patient_count = doctors_appointment_history.values('patient_id').distinct().count()
    total_appointment_count = len(doctors_appointment_history)
    return render(request, 'book_appointment.html', {
        'selected_date': selected_date,
        'appointments': appointments,
        'doctor': doctor,
        'unique_patient_count': unique_patient_count,
        'total_appointment_count': total_appointment_count
    })

def insurance_list(request):
    insurance_list = InsuranceDetails.objects.all()
    return render(request, 'insurance_list.html', {'insurance_list': insurance_list})

def insurance_description(request, insurance_id):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    if request.method=='POST':
        insuranceid = request.POST.get('insurance_id')
        insurance_detail = InsuranceDetails.objects.get(id=insuranceid)
        
        purchase_detail = InsurancePurchaseHistory(provider=insurance_detail.provider, insuranceid=insurance_detail, customer=request.user, datepurchased=date.today())
        purchase_detail.save()
        return redirect('patient_dashboard')
    insurance = InsuranceDetails.objects.get(id=insurance_id)
    return render(request, 'insurance_description.html', {'insurance': insurance})

def all_insurances(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    purchased_insurance_list = InsurancePurchaseHistory.objects.filter(customer=request.user)
    insurance_list = InsuranceDetails.objects.all()
    if request.method == 'POST':
        claimrequested = request.POST.get('claimrequested')
        cancelrequest = request.POST.get('cancelrequest')
        if cancelrequest is not None:
            insurance = InsurancePurchaseHistory.objects.get(id=cancelrequest)
            insurance.claim = 'notclaimed'
            insurance.save()
            return render(request, 'all_insurances.html', {'insurance_list': insurance_list, 'purchased_insurance_list': purchased_insurance_list, 'purchased_insurance_list_count': len(purchased_insurance_list)})

        if claimrequested is not None:
            insurance = InsurancePurchaseHistory.objects.get(id=claimrequested)
            insurance.claim = 'requested'
            insurance.save()
            return render(request, 'all_insurances.html', {'insurance_list': insurance_list, 'purchased_insurance_list': purchased_insurance_list, 'purchased_insurance_list_count': len(purchased_insurance_list)})

    
    return render(request, 'all_insurances.html', {'insurance_list': insurance_list, 'purchased_insurance_list': purchased_insurance_list, 'purchased_insurance_list_count': len(purchased_insurance_list)})

def patient_profile(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    
    appointments = Appointment.objects.filter(patient_id=request.user)
    return render(request, 'patient_profile.html', {'appointments': appointments})
