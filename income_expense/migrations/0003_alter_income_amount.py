# Generated by Django 4.2.2 on 2023-06-18 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_expense', '0002_alter_income_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.CharField(default=10000, max_length=10),
            preserve_default=False,
        ),
    ]