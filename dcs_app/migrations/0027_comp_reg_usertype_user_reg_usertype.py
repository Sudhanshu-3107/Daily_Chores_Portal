# Generated by Django 5.0.4 on 2024-06-01 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcs_app', '0026_jobapplication_visibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='comp_reg',
            name='usertype',
            field=models.CharField(default='company', max_length=20),
        ),
        migrations.AddField(
            model_name='user_reg',
            name='usertype',
            field=models.CharField(default='user', max_length=20),
        ),
    ]
