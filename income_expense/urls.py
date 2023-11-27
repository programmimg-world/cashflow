from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('save_income',views.save_income,name='saveincome'),
    path('save_expense',views.save_expense,name='saveexpense'),
    path('summary',views.summary,name='summary'),
    path('logout',views.logout_view,name='logout'),
    path('current_month_details',views.current_month_details,name='current_month_details'),
    path('save-expense-limit/', views.save_expense_limit, name='save_expense_limit'),
    # path('export-csv/',views.export_data_to_csv, name='export_csv'),
]