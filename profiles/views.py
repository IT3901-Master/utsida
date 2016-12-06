from ajax_select.fields import AutoCompleteField, autoselect_fields_check_can_add
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
import json
from django.http import Http404
from django.views.generic import ListView

from profiles.forms import UserForm, ProfileForm, UpdateUserForm
from .models import *


@login_required
def get_user_profile(request, username):
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
            profile_form = ProfileForm(request.POST,
                                       instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()  # Gracefully save the form
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'], )
            login(request, new_user)
            messages.success(request, 'Your account was succesfully created')
            return redirect('index')
            # else:
            # Could add a message error here if wanted
            # messages.error(request, 'Please correct the error below.')
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
            profile_form.save()
            messages.success(request, 'Profilen din ble endret!')
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

    if (courses):
        university = courses[0].university
    else:
        university = ""

    home_courses = profile.coursesToTake.all()
    course_matches = profile.saved_course_matches.all()

    return render(request, 'profiles/courses.html',
                  {'courses': courses, 'university': university, 'home_courses': home_courses,
                   'course_matches': course_matches})


@login_required
def save_courses(request):
    if request.method == 'POST':
        selected_courses = json.loads(request.POST.getlist('courses')[0])
        profile = Profile.objects.get(user=request.user)

        for course in selected_courses:
            course_code = course["code"]
            course_name = course["name"]
            course_uni = course["university"]
            course_country = course["country"]

            if profile.saved_courses.filter(code=course_code):
                return HttpResponse(json.dumps({
                    'error': 'illegal course',
                    'message': 'Ett eller fler av fagene du prøvde å legge til er allerede lagret.'
                }))

            if not profile.saved_courses.all().filter(
                    university=University.objects.all().filter(name=course_uni)) and profile.saved_courses.all():
                return HttpResponse(json.dumps({
                    'error': 'illegal university',
                    'message': 'Nye valgte fag må være fra samme universitet som dine tidligere lagrede fag.'
                }))

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

        return HttpResponse(json.dumps({
            'code': 200,
            'message': "De valgte fagene er nå lagret i dine 'Lagrede fag', under profilen din. "
        }))
    else:
        return HttpResponse(json.dumps({
            'code': 500,
            'message': 'request is not a post request'
        }))

@login_required
def remove_course(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        course_id = request.POST['id']
        profile.saved_courses.remove(profile.saved_courses.get(id=course_id))
        profile.save()

        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


@login_required
def remove_course_match(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        course_match_id = request.POST['id']
        profile.saved_course_matches.remove(profile.saved_course_matches.get(id=course_match_id))
        profile.save()
        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


@login_required
def remove_all_courses(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.saved_courses.all().delete()
        profile.save()

        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


def university_exists(u):
    for uni in University.objects.all():
        if uni.name == u:
            return True
    return False

@login_required
def send_applation(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        comment = request.POST["comment"]
        course_approval_request = Application(user=user, comment=comment)
        course_approval_request.save()
        course_approval_request.course_matches = user.profile.saved_course_matches.all()
        return HttpResponse({'code': 200, 'message': 'OK'})

@login_required
def save_course_match(request):
    if request.method== "POST":
        homeCode = request.POST["homeCourseCode"]
        abroadCode = request.POST["abroadCourseCode"]
        stored_course_match = CourseMatch.objects.filter(abroadCourse__code=abroadCode,homeCourse__code=homeCode)
        user = User.objects.get(username=request.user)
        hasMatch = user.profile.saved_course_matches.all().filter(abroadCourse__code=abroadCode,homeCourse__code=homeCode)
        if (stored_course_match and hasMatch):
            return HttpResponse(status=409)
        elif (stored_course_match and not hasMatch):
            user.profile.saved_course_matches.add(stored_course_match[0])
            return HttpResponse({'code': 200, 'message': 'Match lagret i profil'})
        elif (not stored_course_match and not hasMatch):
            abroad_course = AbroadCourse.objects.get(code=abroadCode)
            home_course = HomeCourse.objects.get(code=homeCode)
            course_match = CourseMatch(abroadCourse=abroad_course,homeCourse=home_course)
            course_match.save()
            user.profile.saved_course_matches.add(course_match)
            return HttpResponse({'code': 200, 'message': 'Match lagret i profil og database'})

def save_course_match_id(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        id = request.POST["id"]
        stored_course_match = get_object_or_404(CourseMatch,id=id)
        hasMatch = user.profile.saved_course_matches.all().filter(id=id)
        if (hasMatch):
            return HttpResponse(status=409)
        else:
            user.profile.saved_course_matches.add(stored_course_match)
            return HttpResponse({'code': 200, 'message': 'Match lagret i profil'})

@login_required
def view_applications(request):
    user = User.objects.get(request.user)
    applications = Application.objects.filter(user=user)


class ApplicationListView(ListView):
    model = Application

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data(**kwargs)
        return context
