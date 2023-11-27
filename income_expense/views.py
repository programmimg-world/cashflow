from django.shortcuts import render, redirect
from user.models import Userdata, Income, Expense,ExpenseLimit
from user.models import *
from .models import *
from user.views import login_required
from user.models import Income,Expense
from datetime import datetime, timedelta
import calendar
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import csv
# from django.views.decorators.cache import never_cache


@login_required
# implement if only needed view leak issue
# @never_cache  
def main(request):
     print("Inside my_view function")  # Debug statement to check working
     return render(request, 'main.html')


from datetime import datetime

@login_required
def save_income(request):
    if request.method == 'POST':
        fmail = request.session.get('email')
        user = Userdata.objects.get(email=fmail)
        Source1 = request.POST.get('income_source_1')
        Source2 = request.POST.get('income_source_2')
        Other = request.POST.get('other_income')

        now = datetime.now()
        month = now.month
        year = now.year

        income = Income(user=user, month=month, year=year, source_1=Source1, source_2=Source2, other=Other)
        income.save()

        return render(request, 'main.html')
    else:
        error_message = 'Data not saved'
        return render(request, 'login.html', {'error_message': error_message})



from datetime import datetime

@login_required
def save_expense(request):
    fmail = request.session.get('email')
    user = Userdata.objects.get(email=fmail)
    if request.method == 'POST':
        Rent = request.POST.get('rent')
        Electric = request.POST.get('electric')
        Gas = request.POST.get('gas')
        Cell_phone = request.POST.get('cell_phone')
        Groceries = request.POST.get('groceries')
        Car_payment = request.POST.get('car_payment')
        Credit_cards = request.POST.get('credit_cards')
        Auto_insurance = request.POST.get('auto_insurance')
        Miscellaneous = request.POST.get('miscellaneous')

        now = datetime.now()
        month = now.month
        year = now.year

        expense = Expense(user=user, month=month, year=year, rent=Rent, electric=Electric, gas=Gas, cell_phone=Cell_phone,
                          groceries=Groceries, car_payment=Car_payment, credit_cards=Credit_cards,
                          auto_insurance=Auto_insurance, miscellaneous=Miscellaneous)
        expense.save()

        return render(request, 'main.html')
    else:
        error_message = 'Data not saved'
        return render(request, 'login.html', {'error_message': error_message})

@login_required
def summary(request):
    fmail = request.session.get('email')
    user = Userdata.objects.get(email=fmail)
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Calculate the values for each month and year
    monthly_details = []
    yearly_summary = {}

    now = datetime.now()

    # Calculate the values for the selected month and year
    income = Income.objects.filter(user=user, month=selected_month, year=selected_year).aggregate(total=Sum('source_1') + Sum('source_2') + Sum('other'))
    expenses = Expense.objects.filter(user=user, month=selected_month, year=selected_year).aggregate(total=Sum('rent') + Sum('electric') + Sum('gas') + Sum('cell_phone') + Sum('groceries') + Sum('car_payment') + Sum('credit_cards') + Sum('auto_insurance') + Sum('miscellaneous'))

    total_income = income['total'] if income['total'] else 0
    total_expenses = expenses['total'] if expenses['total'] else 0
    total_savings = total_income - total_expenses
    cash_balance = total_income - total_expenses

    if total_income != 0 or total_expenses != 0:
        # Add the monthly details to the list
        monthly_details.append({
            'month': calendar.month_name[int(selected_month)],
            'year': str(selected_year),
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'cash_balance': cash_balance,
        })

    # Move to the previous month
    now -= relativedelta(months=1)

    # Calculate the values for previous years
    current_year = datetime.now().year
    for year in range(current_year - 10, current_year + 100):
        yearly_income = 0
        yearly_expenses = 0
        yearly_savings = 0

        # Check if there is any data for the year
        has_data = Income.objects.filter(user=user, year=year).exists() or Expense.objects.filter(user=user, year=year).exists()

        if has_data:
            for month in range(1, 13):
                if not (year == current_year and month == now.month):  # Exclude the current month
                    # Calculate the values for the year and month
                    income = Income.objects.filter(user=user, month=month, year=year).aggregate(total=Sum('source_1') + Sum('source_2') + Sum('other'))
                    expenses = Expense.objects.filter(user=user, month=month, year=year).aggregate(total=Sum('rent') + Sum('electric') + Sum('gas') + Sum('cell_phone') + Sum('groceries') + Sum('car_payment') + Sum('credit_cards') + Sum('auto_insurance') + Sum('miscellaneous'))

                    total_income = income['total'] if income['total'] else 0
                    total_expenses = expenses['total'] if expenses['total'] else 0
                    total_savings = total_income - total_expenses
                    cash_balance = total_income - total_expenses

                    if total_income != 0 or total_expenses != 0:
                        # Add the monthly details to the list
                        monthly_details.append({
                            'month': calendar.month_name[month],
                            'year': str(year),
                            'total_income': total_income,
                            'total_expenses': total_expenses,
                            'total_savings': total_savings,
                            'cash_balance': cash_balance,
                        })

                    # Calculate yearly totals
                    yearly_income += total_income
                    yearly_expenses += total_expenses
                    yearly_savings += total_savings

            # Add yearly summary to the dictionary
            yearly_summary[str(year)] = {
                'total_income': yearly_income,
                'total_expenses': yearly_expenses,
                'total_savings': yearly_savings,
                'cash_balance': yearly_income - yearly_expenses
            }

    # Sort the monthly_details list based on year and month in descending order
    monthly_details.sort(key=lambda x: (int(x['year']), list(calendar.month_name).index(x['month'])), reverse=True)

    return render(request, 'summary.html', {
        'monthly_details': monthly_details,
        'yearly_summary': yearly_summary
    })

@login_required
def current_month_details(request):
    now = datetime.now()
    month = now.month
    year = now.year

    # Retrieve the email from the session
    email = request.session.get('email')

    # Retrieve the user using the email
    user = Userdata.objects.get(email=email)

    # Calculate the sum of expenses for each field in the current month and user
    expense_sums = Expense.objects.filter(user=user, month=month, year=year).aggregate(
        rent_sum=Sum('rent'),
        electric_sum=Sum('electric'),
        gas_sum=Sum('gas'),
        cell_phone_sum=Sum('cell_phone'), 
        groceries_sum=Sum('groceries'),
        car_payment_sum=Sum('car_payment'),
        credit_cards_sum=Sum('credit_cards'),
        auto_insurance_sum=Sum('auto_insurance'),
        miscellaneous_sum=Sum('miscellaneous')
    )

    # Calculate the sum of income for each field in the current month and user
    income_sums = Income.objects.filter(user=user, month=month, year=year).aggregate(
        source_1_sum=Sum('source_1'),
        source_2_sum=Sum('source_2'),
        other_sum=Sum('other')
    )
    email = request.session.get('email') # Assuming the user is logged in
    now = datetime.now()
    month = now.month
    year = now.year

    # Retrieve the user based on their email
    user = Userdata.objects.get(email=email)

    # Retrieve the expense limits for the user based on the month and year
    expense_limits = ExpenseLimit.objects.filter(user=user, month=month, year=year).aggregate(
        rent_limit=Sum('rent_limit'),
        electric_limit=Sum('electric_limit'),
        gas_limit=Sum('gas_limit'),
        cell_phone_limit=Sum('cell_phone_limit'),
        groceries_limit=Sum('groceries_limit'),
        car_payment_limit=Sum('car_payment_limit'),
        credit_cards_limit=Sum('credit_cards_limit'),
        auto_insurance_limit=Sum('auto_insurance_limit'),
        miscellaneous_limit=Sum('miscellaneous_limit'))

    context = {
        'expense_sums': expense_sums,
        'income_sums': income_sums,
        'expense_limits': expense_limits,
    }

    return render(request, 'current_month_details.html', context)

def save_expense_limit(request):
    fmail = request.session.get('email')
    User = Userdata.objects.get(email=fmail)
    if request.method == 'POST':
        # Retrieve the form data from the request
        rent_limit = request.POST.get('rent_limit')
        electric_limit = request.POST.get('electric_limit')
        gas_limit = request.POST.get('gas_limit')
        cell_phone_limit = request.POST.get('cell_phone_limit')
        groceries_limit = request.POST.get('groceries_limit')
        car_payment_limit = request.POST.get('car_payment_limit')
        credit_cards_limit = request.POST.get('credit_cards_limit')
        auto_insurance_limit = request.POST.get('auto_insurance_limit')
        miscellaneous_limit = request.POST.get('miscellaneous_limit')

        # Create an ExpenseLimit instance and save it to the database
        expense_limit = ExpenseLimit(
            user=User,
            rent_limit=rent_limit,
            electric_limit=electric_limit,
            gas_limit=gas_limit,
            cell_phone_limit=cell_phone_limit,
            groceries_limit=groceries_limit,
            car_payment_limit=car_payment_limit,
            credit_cards_limit=credit_cards_limit,
            auto_insurance_limit=auto_insurance_limit,
            miscellaneous_limit=miscellaneous_limit
        )
        expense_limit.save()

        return redirect('current_month_details')
    else:
        # Render the form template if the request method is not POST
        return render(request, 'current_month_details')

def logout_view(request):
    request.session.clear()
    # Check if session data is cleared
    if 'email' not in request.session:
        print('Session data cleared successfully')
    else:
        print('Session data not cleared')
    return redirect('login')

# def export_data_to_csv(request):
#     # Query the data from the models
#     userdata = Userdata.objects.all()
#     incomes = Income.objects.all()
#     expenses = Expense.objects.all()

#     # Define the CSV file name
#     filename = "data_export.csv"

#     # Create the HTTP response object with CSV content type
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

#     # Create the CSV writer
#     writer = csv.writer(response)

#     # Write the header row for userdata
#     writer.writerow(['Email', 'Name', 'Password'])

#     # Write userdata rows
#     for user in userdata:
#         writer.writerow([user.email, user.name, user.password])

#     # Write the header row for income and expense
#     writer.writerow([])
#     writer.writerow(['User Email', 'Month', 'Year', 'Source 1', 'Source 2', 'Other', 'Rent', 'Electric', 'Gas', 'Cell Phone', 'Groceries', 'Car Payment', 'Credit Cards', 'Auto Insurance', 'Miscellaneous'])

    # Combine income and expense data
    # data_rows = []
    # for income, expense in zip(incomes, expenses):
    #     data_row = [income.user.email, income.month, income.year, income.source_1, income.source_2, income.other,
    #                 expense.rent, expense.electric, expense.gas, expense.cell_phone, expense.groceries,
    #                 expense.car_payment, expense.credit_cards, expense.auto_insurance, expense.miscellaneous]
    #     data_rows.append(data_row)

    # # Write the combined data rows
    # for data_row in data_rows:
    #     writer.writerow(data_row)

    # return response


