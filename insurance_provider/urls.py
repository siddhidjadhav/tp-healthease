from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.insurance_dashboard, name="insurance_dashboard"),
    path('insurance_detail/<insurance_id>', views.insurance_detail, name="insurance_detail"),
    path('delete_insurance/<insurance_id>', views.delete_insurance, name="delete_insurance"),
]