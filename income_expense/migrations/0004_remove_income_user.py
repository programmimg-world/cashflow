# Generated by Django 4.2.2 on 2023-06-19 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income_expense', '0003_alter_income_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='income',
            name='user',
        ),
    ]