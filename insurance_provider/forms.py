from django import forms
from django.forms import ModelForm
from .models import Insurance, InsuranceDetails

#Create a Insurance form
class InsuranceForm(ModelForm):
    class Meta:
        model = Insurance
        fields = ('insurance_name', 'validity', 'coverage')
        labels = {
            'insurance_name': '',
            'validity': '',
            'coverage': ''
        }
        widgets = {
            'insurance_name': forms.TextInput(attrs={'placeholder': 'Insurance Name', 'class': 'form-control'}),
            'validity': forms.NumberInput(attrs={'placeholder': 'Valid Until', 'class': 'form-control'}),
            'coverage': forms.NumberInput(attrs={'placeholder': 'Claim Coverage', 'class': 'form-control'})
        }

class InsuranceDetailForm(ModelForm):
    class Meta:
        model = InsuranceDetails
        fields = ('name', 'coverage', 'description')
        labels = {
            'name': '',
            'coverage': '',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Insurance Name', 'class': 'form-control'}),
            'coverage': forms.NumberInput(attrs={'placeholder': 'Claim Coverage', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control'})
        }