# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-17 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20161031_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='savedCourses',
            field=models.TextField(null=True),
        ),
    ]
