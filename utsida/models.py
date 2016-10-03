from django.db import models

CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Faculty(models.Model):
    acronym = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.acronym + ' - ' + self.name


class Institute(models.Model):
    acronym = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty)

    def __str__(self):
        return self.acronym + ' - ' + self.name


class Country(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class AbroadCourse(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=50)
    university = models.ForeignKey(University)

    def __str__(self):
        return self.code + ' - ' + self.name


class HomeCourse(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=50)
    description_url = models.URLField(max_length=2000, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self


class CourseMatch(models.Model):
    homeCourse = models.ForeignKey(HomeCourse)
    abroadCourse = models.ForeignKey(AbroadCourse)

    def __str__(self):
        return self.homeCourse.code + " - " + self.abroadCourse.code


class Case(models.Model):
    homeInstitute = models.ForeignKey(Institute)
    country = models.ForeignKey(Country)
    university = models.ForeignKey(University)
    studyPeriod = models.IntegerField()
    language = models.CharField(max_length=30)
    academicQualityRating = models.IntegerField(choices=CHOICES)
    socialQualityRating = models.IntegerField(choices=CHOICES)
    subjects = models.ManyToManyField(AbroadCourse)

    def __str__(self):
        return self.university.name + ':' + str(self.pk)


class Query(models.Model):
    homeInstitute = models.ForeignKey(Institute)
    country = models.ForeignKey(Country)
    university = models.ForeignKey(University)
    studyPeriod = models.IntegerField()
    language = models.CharField(max_length=30)
    academicQualityRating = models.IntegerField(choices=CHOICES)
    socialQualityRating = models.IntegerField(choices=CHOICES)

    def __str__(self):
        return self.university.name + ':' + str(self.pk)
