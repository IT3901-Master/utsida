# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utsida', '0004_auto_20160929_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homecourse',
            name='id',
        ),
        migrations.AlterField(
            model_name='homecourse',
            name='code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
