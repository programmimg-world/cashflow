# Generated by Django 4.2.2 on 2023-06-19 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_expense', '0004_remove_income_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='discription',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
