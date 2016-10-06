from django.contrib.auth.models import User
from django.db import models
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from utsida.models import *
from django.contrib.auth.signals import user_logged_in, user_logged_out


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, null=True)
    coursesTaken = models.ManyToManyField(HomeCourse)

    class Meta:
        verbose_name_plural = 'profiles'
        verbose_name = 'profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def send_login_message(sender, user, request, **kwargs):
    messages.success(request,'You were succesfully logged in')


def send_logout_message(sender, user, request, **kwargs):
    messages.success(request,'You were succesfully logged out')

user_logged_out.connect(send_logout_message)
user_logged_in.connect(send_login_message)