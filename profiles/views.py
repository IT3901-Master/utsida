from ajax_select.fields import AutoCompleteField, autoselect_fields_check_can_add
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
import json

from profiles.forms import UserForm, ProfileForm, UpdateUserForm
from .models import *



# Create your views here.
@login_required
def get_user_profile(request,username):
    user = User.objects.get(username=username)
    context = {"user": user}
    return render(request, 'profiles/user_profile.html', context)


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
            new_user = authenticate(username=user_form.cleaned_data['username'],password=user_form.cleaned_data['password1'],)
            login(request, new_user)
            messages.success(request, 'Your account was succesfully created')
            return redirect('index')
        #else:
            #Could add a message error here if wanted
            #messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'profiles/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #user.refresh_from_db()
            profile_form.save()
            messages.success(request, 'Profilen din ble endret!')
            #login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Vennligst rett feilen under.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Passordet ditt ble endret!')
            return redirect('index')
        else:
            messages.error(request, 'Vennligst rett feilen under.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {
        'form': form
    })


@login_required
def saved_courses(request):
    profile = Profile.objects.get(user=request.user)

    courses = profile.saved_courses.all()

    return render(request, 'profiles/courses.html', {'courses': courses})


def save_courses(request):
    if request.method == 'POST':
        selected_courses = json.loads(request.POST.getlist('courses')[0])
        profile = Profile.objects.get(user=request.user)

        for course in selected_courses:
            course_code = course["code"]
            course_name = course["name"]
            course_uni = course["university"]
            course_country = course["country"]

            if AbroadCourse.objects.all().filter(code=course_code):
                new_course = AbroadCourse.objects.get(code=course_code)
                profile.saved_courses.add(new_course)
                profile.save()

            else:
                if not university_exists(course_uni):
                    new_uni = University.objects.create(
                        name=course_uni,
                        country=Country.objects.get(name=course_country)
                    )
                    new_abroad_course = AbroadCourse(
                        code=course_code,
                        name=course_name,
                        university=new_uni
                    )
                else:
                    new_abroad_course = AbroadCourse(
                        code=course_code,
                        name=course_name,
                        university=University.objects.get(name=course_uni)
                    )

                new_abroad_course.save()
                profile.saved_courses.add(new_abroad_course)
                profile.save()

        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


def university_exists(u):
    for uni in University.objects.all():
        if uni.name == u:
            return True
    return False
