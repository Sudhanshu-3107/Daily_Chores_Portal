# Generated by Django 5.0.1 on 2024-04-14 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcs_app', '0023_employee_booking_payment_alter_feedback_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_booking',
            name='payment',
            field=models.FileField(upload_to='Dailychores_Security/Payment_Screenshots/'),
        ),
    ]