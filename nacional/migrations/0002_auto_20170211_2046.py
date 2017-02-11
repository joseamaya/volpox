# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-11 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nacional', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actacongresal',
            name='mesa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nacional.MesaNacional'),
        ),
        migrations.AlterField(
            model_name='actapresidencial',
            name='mesa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nacional.MesaNacional'),
        ),
    ]