# Generated by Django 4.2.2 on 2023-06-24 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_expense_month_expense_year_income_month_income_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='year',
            field=models.IntegerField(default=2023),
        ),
        migrations.AlterField(
            model_name='income',
            name='year',
            field=models.IntegerField(default=2023),
        ),
    ]
