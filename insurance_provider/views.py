from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import InsuranceDetailForm
from django.contrib import messages
from .models import Insurance, InsuranceDetails, InsurancePurchaseHistory
import re

def insurance_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    user = request.user.email
    # email = ""
    # if re.search(".@gmail.com$", user):
    #     email = "yes" 
    #     return redirect('patient_dashboard')
    submitted = False

    if request.method == "POST":
        if request.POST.get('cancelrequest') is not None:
            insurance = InsurancePurchaseHistory.objects.get(id=request.POST.get('cancelrequest'))
            insurance.claim = 'cancelled'
            insurance.cancellationreason = request.POST.get('reason')
            insurance.save()
            return redirect('insurance_dashboard')
        
        if request.POST.get('claimaccepted') is not None:
            insurance = InsurancePurchaseHistory.objects.get(id=request.POST.get('claimaccepted'))
            insurance.claim = 'accepted'
            insurance.save()
            return redirect('insurance_dashboard')

        form = InsuranceDetailForm(request.POST)
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.provider = request.user
            insurance.save()
            # form.save()
            return HttpResponseRedirect('/insurance_provider/dashboard?submitted=True')
        
    else:
        form = InsuranceDetailForm
        if 'submitted' in request.GET:
            submitted = True
            messages.success(request, ("New Insurance added Successfully"))

    insurance_list = InsuranceDetails.objects.filter(provider=request.user)
    claimed_insurances_list = InsurancePurchaseHistory.objects.filter(provider=request.user, claim='requested')

    count = 0
    for insurance in insurance_list:
        count = count+1
        insurance.display_id = count
    return render(request, 'insurance_dashboard.html', {'form': form, 'submitted': submitted, 'insurance_list': insurance_list, 'claimed_insurances_list': claimed_insurances_list})

def insurance_detail(request, insurance_id):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    insurance = InsuranceDetails.objects.get(pk=insurance_id)
    purchase_history = InsurancePurchaseHistory.objects.filter(insuranceid=insurance)
    return render(request, 'insurance_detail.html', {'insurance': insurance, 'purchase_history': purchase_history})

def delete_insurance(request, insurance_id):
    if not request.user.is_authenticated:
        return redirect(f"{'/users/login'}?next={request.path}")
    insurance = InsuranceDetails.objects.get(pk=insurance_id)
    insurance.delete()
    messages.info(request, ("Insurance Deleted"))
    return redirect('insurance_dashboard')

