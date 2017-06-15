# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankMonitor', '0002_auto_20170530_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='is_central',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='trans',
            name='date',
            field=models.DateTimeField(default=''),
        ),
    ]