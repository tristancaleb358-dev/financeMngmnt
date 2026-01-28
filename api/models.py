from django.db import models

# Create your models here.

class BASIC(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        ordering = ["created_at"]


class CUSTOMER(BASIC):
    first_name = models.CharField(max_length=200, null=False)  
    last_name = models.CharField(max_length=200)  
    address = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(unique=True, null=False)  
    mobile = models.CharField(max_length=10, null=False)
    password = models.CharField(max_length=300, null=False)
    date_of_birth = models.DateField(null=False, blank=True)
    class AbonnementType(models.TextChoices):
        FREE = "FREE", "Free"
        BASIC = "BASIC", "Basic"
        PREMIUM = "PREMIUM", "Premium"

    abonnement_type = models.CharField(
        max_length=20,
        choices=AbonnementType.choices,
        default=AbonnementType.FREE,
        null=False
    )
    status = models.BooleanField(default=True)
    class CustomerType(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "EMPLOYEE"
        JOBLESS = "JOBLESS", "JOBLESS"
    customer_type = models.CharField(
        max_length=20,
        choices=CustomerType.choices,
        default=CustomerType.JOBLESS,null=False)
  
    def __str__(self):  
        return self.first_name + " " + self.last_name  
