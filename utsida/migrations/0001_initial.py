# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 10:46
# Generated by Django 1.10.1 on 2016-10-18 11:15

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbroadCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('description_url', models.URLField(blank=True, default='', max_length=2000)),
                ('study_points', models.FloatField(blank=True, default=7.5)),
                ('pre_requisites', models.ManyToManyField(blank=True, related_name='_abroadcourse_pre_requisites_+', to='utsida.AbroadCourse')),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(max_length=30)),
                ('studyPeriod', models.IntegerField()),
                ('academicQualityRating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('socialQualityRating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('continent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Continent')),
            ],
        ),
        migrations.CreateModel(
            name='CourseMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=200)),
                ('abroadCourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.AbroadCourse')),
            ],
            options={
                'verbose_name': 'course match',
                'verbose_name_plural': 'course matches',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('acronym', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'faculties',
            },
        ),
        migrations.CreateModel(
            name='HomeCourse',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description_url', models.URLField(blank=True, default='', max_length=2000)),
            ],
            options={
                'verbose_name': 'home course',
                'verbose_name_plural': 'home courses',
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('acronym', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(max_length=30)),
                ('studyPeriod', models.IntegerField()),
                ('academicQualityRating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('socialQualityRating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('continent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Continent')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Country')),
                ('homeInstitute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Institute')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Language')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'universities',
            },
        ),
        migrations.AddField(
            model_name='coursematch',
            name='homeCourse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.HomeCourse'),
        ),
        migrations.AddField(
            model_name='case',
            name='continent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Continent'),
        ),
        migrations.AddField(
            model_name='case',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Country'),
        ),
        migrations.AddField(
            model_name='case',
            name='homeInstitute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Institute'),
        ),
        migrations.AddField(
            model_name='case',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.Language'),
        ),
        migrations.AddField(
            model_name='case',
            name='subjects',
            field=models.ManyToManyField(to='utsida.AbroadCourse'),
        ),
        migrations.AddField(
            model_name='abroadcourse',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utsida.University'),
        ),
        migrations.AlterUniqueTogether(
            name='abroadcourse',
            unique_together=set([('code', 'university')]),
        ),
    ]
