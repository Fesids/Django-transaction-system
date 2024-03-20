from django.db import models

# Create your models here.

class Client(models.Model):
    CLIENT_TIER = [('basic', 'Basic'), ('premium', 'Premium')]
    CPF = models.CharField(max_length=25, blank=False, null=False)
    tier = models.CharField(max_length=20, default='basic', choices=CLIENT_TIER)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=19)
    company_id = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True) 
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'clients'