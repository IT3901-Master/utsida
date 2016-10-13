from django.contrib.auth.models import User
from django.db import models
import datetime

CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Faculty(models.Model):
    acronym = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.acronym + ' - ' + self.name

    class Meta:
        verbose_name_plural = 'faculties'


class Institute(models.Model):
    acronym = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty)

    def __str__(self):
        return self.acronym + ' - ' + self.name


class Continent(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'countries'


class Country(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    continent = models.ForeignKey(Continent)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'universities'


class AbroadCourse(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    pre_requisites = models.ManyToManyField('self', blank=True)
    university = models.ForeignKey(University)
    description_url = models.URLField(max_length=2000, blank=True,default="")
    study_points = models.FloatField(blank=True, default=7.5)

    class Meta:
        unique_together = ["code","university"]

    def __str__(self):
        return self.code + ' - ' + self.name


class HomeCourse(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    description_url = models.URLField(max_length=2000, blank=True,default="")

    def __str__(self):
        return self.pk + ' - ' + self.name


    class Meta:
        verbose_name_plural = 'home courses'
        verbose_name = 'home course'


class CourseMatch(models.Model):
    homeCourse = models.ForeignKey(HomeCourse)
    abroadCourse = models.ForeignKey(AbroadCourse)
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(blank=True,null=True)
    comment = models.CharField(max_length=200,blank=True,default="")

    def __str__(self):
        return self.homeCourse.code + ' - ' + self.abroadCourse.pk

    class Meta:
        verbose_name_plural = 'course matches'
        verbose_name = 'course match'


class Language(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name


class Case(models.Model):
    homeInstitute = models.ForeignKey(Institute)
    continent = models.ForeignKey(Continent)
    country = models.ForeignKey(Country)
    university = models.CharField(max_length=30)
    studyPeriod = models.IntegerField()
    language = models.ForeignKey(Language)
    academicQualityRating = models.IntegerField(choices=CHOICES)
    socialQualityRating = models.IntegerField(choices=CHOICES)
    subjects = models.ManyToManyField(AbroadCourse)

    def __str__(self):
        return self.university + ':' + str(self.pk)


class Query(models.Model):
    homeInstitute = models.ForeignKey(Institute)
    continent = models.ForeignKey(Continent)
    country = models.ForeignKey(Country)
    university = models.CharField(max_length=30)
    studyPeriod = models.IntegerField()
    language = models.ForeignKey(Language)
    academicQualityRating = models.IntegerField(choices=CHOICES)
    socialQualityRating = models.IntegerField(choices=CHOICES)

    def __str__(self):
        return self.university + ':' + str(self.pk)
