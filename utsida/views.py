from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from utsida.forms import UserForm, ProfileForm
from .models import *
import json


def index(request):
    return render(request, "utsida/index.html")


def process(request):
    institute_list = Institute.objects.all()
    faculty_list = Faculty.objects.all()
    university_list = University.objects.all()

    context = {"institute_list" : institute_list, "faculty_list":faculty_list, "university_list" :university_list}
    return render(request, "utsida/process.html", context)



def courseMatch(request):
    if request.user.is_authenticated():
        course_matches = CourseMatch.objects.all()
        context = {"course_match_list": course_matches}
    else:
        context = {}
    return render(request,"utsida/courseMatch.html",context)

@login_required
def get_user_profile(request,username):
    user = User.objects.get(username=username)
    context = {"user": user}
    return render(request, 'utsida/user_profile.html', context)


class MyRegistrationForm(object):
    pass

@transaction.atomic
def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = ProfileForm(request.POST, instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()  # Gracefully save the form
            HttpResponseRedirect("/register_success")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'utsida/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def register_success(request):
    return render(request,'utsida/register_success.html', {})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('register_success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'utsida/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })