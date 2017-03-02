from django.contrib.auth.models import User
from django.db import models
import datetime


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


class UniversityManager(models.Manager):
    def get_by_natural_key(self, name):
        print(name)
        return self.get(name=name)


class University(models.Model):
    name = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=10, blank=True)
    country = models.ForeignKey(Country, blank=True)
    objects = UniversityManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    class Meta:
        verbose_name_plural = 'universities'


class AbroadCourseManager(models.Manager):
    def get_by_natural_key(self, code, name, university):
        return self.get(code=code, name=name, university__name=university)


class AbroadCourse(models.Model):
    code = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=50)
    pre_requisites = models.ManyToManyField('self', blank=True)
    university = models.ForeignKey(University)
    description_url = models.URLField(max_length=2000, blank=True,default="")
    study_points = models.FloatField(blank=True, default=7.5)
    objects = AbroadCourseManager()

    class Meta:
        unique_together = ["code", "name", "university"]

    def __str__(self):
        return self.code + ' ' + self.name

    def natural_key(self):
        return self.code, self.name, self.university


class HomeCourseManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class HomeCourse(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    description_url = models.URLField(max_length=2000, blank=True,default="")
    objects = HomeCourseManager()

    def __str__(self):
        return self.code + ' - ' + self.name

    class Meta:
        verbose_name_plural = 'home courses'
        verbose_name = 'home course'

    def natural_key(self):
        return (self.code,)


class CourseMatchManager(models.Manager):
    def get_by_natural_key(self,homeCourse,abroadCourse):
        return self.get(homeCourse=homeCourse,abroadCourse=abroadCourse)


class CourseMatch(models.Model):
    homeCourse = models.ForeignKey(HomeCourse)
    abroadCourse = models.ForeignKey(AbroadCourse)
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(blank=True,null=True)
    comment = models.CharField(max_length=200,blank=True,default="")
    objects = CourseMatchManager()

    def __str__(self):
        return self.homeCourse.code + ' - ' + self.abroadCourse.code

    class Meta:
        verbose_name_plural = 'course matches'
        verbose_name = 'course match'
        unique_together = ["homeCourse","abroadCourse"]

    def natural_key(self):
        return (self.homeCourse,self.abroadCourse)


class Language(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name


STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('D', 'Disapproved'),
    )

class Application(models.Model):
    user = models.ForeignKey(User)
    course_matches = models.ManyToManyField(CourseMatch)
    comment = models.CharField(max_length=400,blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default="P")


CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10))


class Case(models.Model):
    homeInstitute = models.ForeignKey(Institute)
    continent = models.ForeignKey(Continent)
    country = models.ForeignKey(Country)
    university = models.CharField(max_length=30)
    studyPeriod = models.IntegerField()
    language = models.ForeignKey(Language)
    academicQualityRating = models.IntegerField(choices=CHOICES)
    socialQualityRating = models.IntegerField(choices=CHOICES)
    residentialQualityRating = models.IntegerField(choices=CHOICES)
    receptionQualityRating = models.IntegerField(choices=CHOICES)
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
    residentialQualityRating = models.IntegerField(choices=CHOICES)
    receptionQualityRating = models.IntegerField(choices=CHOICES)

    def __str__(self):
        return self.university + ':' + str(self.pk)
