# Generated by Django 5.0.1 on 2024-04-10 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcs_app', '0007_alter_hiring_job_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiring',
            name='job_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dcs_app.employee_category'),
        ),
    ]