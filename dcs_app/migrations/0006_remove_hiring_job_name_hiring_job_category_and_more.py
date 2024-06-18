# Generated by Django 5.0.1 on 2024-04-10 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcs_app', '0005_comp_reg_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hiring',
            name='job_name',
        ),
        migrations.AddField(
            model_name='hiring',
            name='job_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcs_app.employee_category'),
        ),
        migrations.AlterField(
            model_name='hiring',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dcs_app.comp_reg'),
        ),
    ]