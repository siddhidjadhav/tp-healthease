from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('create_appointment', views.create_appointment, name="create_appointment"), 
    path('all_appointment', views.appointments_list, name="all_appointment"), 
    path('add_prescription/<appointment_id>', views.add_prescription, name="add_prescription"),
]

