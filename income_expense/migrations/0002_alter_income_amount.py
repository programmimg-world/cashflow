# Generated by Django 4.2.2 on 2023-06-18 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
