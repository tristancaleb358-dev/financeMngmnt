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
    first_name = models.TextField()
    last_name = models.TextField()
    iso2Country = models.TextField()
    iso3Country = models.TextField()
    address = models.TextField()
    email = models.EmailField(unique=True, null=False, blank=False)  
    password = models.CharField(max_length=50, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=True)
    last_name = models.TextField()
    first_name = models.TextField()
    birth_date = models.DateField()
    status = models.CharField(max_length=500, null=False)
    phone = models.CharField(unique= True, max_length=20, null=False, blank=False)
    active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email', 'phone']),
        ]
    def __str__(self):  
        return self.first_name + " " + self.last_name  


# New Models
class IncomeCategory(BASIC):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_recurring = models.BooleanField(default=False)
    periodicity = models.CharField(max_length=50)
    is_fixed = models.BooleanField(default=True)

class Income(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    price = models.JSONField(default=dict)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes')

class ExpenseCategory(BASIC):
    name = models.CharField(max_length=100)
    description = models.TextField()
    budget_limit = models.FloatField()
    periodicity = models.CharField(max_length=50)

class Expense(BASIC):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    price = models.JSONField(default=dict)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expenses')

class SavingsGoal(BASIC):
    class Priority(models.TextChoices):
        P0 = 'P0', 'Priorité Haute'
        P1 = 'P1', 'Priorité Moyenne'
        P2 = 'P2', 'Priorité Basse'

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_target_amount = models.FloatField()
    currency = models.CharField(max_length=3, null=False)
    saving_history = models.JSONField(default=list) # Pour stocker List<Dict>
    priority = models.CharField(max_length=2, choices=Priority.choices)
    user = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)
    income_categories = models.ManyToManyField(IncomeCategory)
    expense_categories = models.ManyToManyField(ExpenseCategory)

class PerformanceMetric(models.Model):
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    indicators = models.JSONField() # Pour stocker List<Dict>
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE)

class Subscription(models.Model):
    name = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)
    price = models.JSONField(default=dict)
    description = models.TextField()
    def __str(self):
        return self.name


class Payment(models.Model):
    period = models.DateField()
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)