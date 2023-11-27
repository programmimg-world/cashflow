from django.db import models
from datetime import datetime


class Userdata(models.Model):
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=8)


    def __str__(self):
        return self.email

class Income(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE,null=True)
    month = models.IntegerField(default=datetime.now().month)
    year = models.IntegerField(default=datetime.now().year)
    source_1 = models.IntegerField(null=True, default=None)
    source_2 = models.IntegerField(null=True, default=None)
    other = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f"Income of {self.user.email if self.user else 'Unknown User'}"



class Expense(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE,null=True)
    month = models.IntegerField(default=datetime.now().month)
    year = models.IntegerField(default=datetime.now().year)
    rent = models.IntegerField(null=True, default=None)
    electric = models.IntegerField(null=True, default=None)
    gas = models.IntegerField(null=True, default=None)
    cell_phone = models.IntegerField(null=True, default=None)
    groceries = models.IntegerField(null=True, default=None)
    car_payment = models.IntegerField(null=True, default=None)
    credit_cards = models.IntegerField(null=True, default=None)
    auto_insurance = models.IntegerField(null=True, default=None)
    miscellaneous = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f"Expense of {self.user.email if self.user else 'Unknown User'}"

class ExpenseLimit(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE, null=True)
    month = models.IntegerField(default=datetime.now().month)
    year = models.IntegerField(default=datetime.now().year)
    rent_limit = models.IntegerField(null=True, default=None)
    electric_limit = models.IntegerField(null=True, default=None)
    gas_limit = models.IntegerField(null=True, default=None)
    cell_phone_limit = models.IntegerField(null=True, default=None)
    groceries_limit = models.IntegerField(null=True, default=None)
    car_payment_limit = models.IntegerField(null=True, default=None)
    credit_cards_limit = models.IntegerField(null=True, default=None)
    auto_insurance_limit = models.IntegerField(null=True, default=None)
    miscellaneous_limit = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f"Expense Limits of {self.user.email if self.user else 'Unknown User'}"
