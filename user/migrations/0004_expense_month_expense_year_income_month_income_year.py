# Generated by Django 4.2.2 on 2023-06-23 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_income_amount_remove_income_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='month',
            field=models.IntegerField(default=6),
        ),
        migrations.AddField(
            model_name='expense',
            name='year',
            field=models.IntegerField(default=6),
        ),
        migrations.AddField(
            model_name='income',
            name='month',
            field=models.IntegerField(default=6),
        ),
        migrations.AddField(
            model_name='income',
            name='year',
            field=models.IntegerField(default=6),
        ),
    ]
