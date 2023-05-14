from django.db import models
from django.contrib.auth.models import User

class Insurance(models.Model):
    insurance_name = models.CharField('Name', max_length=30)
    validity = models.IntegerField('Valid till')
    coverage = models.IntegerField('Coverage')

    # insurance_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.insurance_name
    

class InsuranceDetails(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="provider")
    name = models.CharField('Name', max_length=50)
    coverage = models.IntegerField('Coverage')
    description = models.CharField('Description', max_length=200)

    # insurance_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class InsurancePurchaseHistory(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="insurance_provider")
    insuranceid = models.ForeignKey(InsuranceDetails, on_delete=models.CASCADE, related_name="insurance")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    datepurchased = models.DateField()
    claim = models.CharField(default='notclaimed', max_length=50)
    cancellationreason = models.CharField(max_length=500, blank=True)
    