# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utsida', '0003_auto_20160929_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homecourse',
            name='description_url',
            field=models.URLField(blank=True, max_length=2000),
        ),
    ]
