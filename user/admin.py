from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Userdata)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(ExpenseLimit)