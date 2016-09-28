from django.db import models

CHOICES = ((1,1),(2,2),(3,3),(4,4),(5,5))


class Faculty(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

class Institute(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    faculty = models.ForeignKey(Faculty)


class Country(models.Model):
    name = models.CharField(max_length=30, primary_key=True)


class University(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class Course(models.Model):
    name = models.CharField(max_length=10, primary_key=True)




class Case(models.Model):
    homeInstitute = models.ForeignKey(Institute)
    country = models.ForeignKey(Country)
    university = models.ForeignKey(University)
    studyPeriod = models.IntegerField()
    language = models.CharField(max_length=30)
    academicQualityRating = models.IntegerField(choices=CHOICES)
    specialCompetencyRating = models.IntegerField(choices=CHOICES)
    socialQualityRating = models.IntegerField(choices=CHOICES)
    careerAdvantagesRating = models.IntegerField(choices=CHOICES)
    subjects = models.ManyToManyField(Course)
