from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

CHOICES = ((1,1),(2,2),(3,3),(4,4),(5,5))


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
    specialCompetencyRating = models.IntegerField(choices=CHOICES)
    socialQualityRating = models.IntegerField(choices=CHOICES)
    careerAdvantagesRating = models.IntegerField(choices=CHOICES)
    subjects = models.ManyToManyField(AbroadCourse)

    def __str__(self):
        return self.university.name + ':' + str(self.pk)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute,null=True)
    coursesTaken = models.ManyToManyField(HomeCourse)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



