from ajax_select.fields import AutoCompleteField, autoselect_fields_check_can_add
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
import json
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from profiles.forms import UserForm, ProfileForm, UpdateUserForm, CoursesToTakeForm, ProfileRegisterForm, \
    PasswordChangeCustomForm
from utsida.forms import abroadCourseForm
from .models import *


class MyRegistrationForm(object):
    pass


@transaction.atomic
def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        print(user_form.is_valid())
        print(profile_form.is_valid())
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = ProfileRegisterForm(request.POST,
                                               instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()
            profile_form.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'], )
            login(request, new_user)
            return redirect('index')
        else:
            messages.error(request, "Brukeren ble ikke opprettet, vennligst rett feilene under")
    else:
        user_form = UserForm()
        profile_form = ProfileRegisterForm()
    return render(request, 'registration/register.html', {
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
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Passordet ditt ble endret!')
            return redirect('index')
        else:
            messages.error(request, "Passordet ditt ble ikke endret, vennligst rett feilene")
    else:
        form = PasswordChangeCustomForm(request.user)
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
    abroad_course_form = abroadCourseForm()
    courses_to_take_form = CoursesToTakeForm()

    return render(request, 'profiles/courses.html',
                  {'courses': courses, 'university': university, 'home_courses': home_courses,
                   'course_matches': course_matches, 'add_abroad_form': abroad_course_form,
                   'courses_to_take_form': courses_to_take_form})


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

            if profile.saved_courses.filter(name=course_name):
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

            if AbroadCourse.objects.all().filter(name=course_name, code=course_code,
                                                 university=University.objects.all().filter(name=course_uni)):
                new_course = AbroadCourse.objects.get(name=course_name, code=course_code,
                                                      university=University.objects.get(name=course_uni))
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
def add_abroad_course_to_profile(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        university = get_object_or_404(University, name=request.POST.get('university'))

        course = AbroadCourse.objects.get(code=request.POST.get('code'),university=university)
        if (course):
            if (course in user.profile.saved_courses.all()):
                return HttpResponse(status=409)
            course.full_clean()
            course.save()
        else:
            course = AbroadCourse(code=request.POST.get('code'), name=request.POST.get('name'),
                              study_points=request.POST.get('study_points'), university=university,
                              description_url=request.POST.get('url'))

        response_data = {
            "code": request.POST.get('code'),
            "name": request.POST.get('name'),
            "id": course.pk,
            "university": course.university.name,
            "country": course.university.country.name
        }
        user.profile.saved_courses.add(course)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )




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
def remove_home_course(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        course_id = request.POST.get('id')
        profile.coursesToTake.remove(profile.coursesToTake.get(id=course_id))
        profile.save()

        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


@login_required
def remove_course_match(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        course_match_id = request.POST.get('id')
        profile.saved_course_matches.remove(profile.saved_course_matches.get(pk=course_match_id))
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
    if request.method == "POST":
        homeCode = request.POST["homeCourseCode"]
        abroadCode = request.POST["abroadCourseCode"]
        abroad_name = request.POST["abroadCourseName"]
        stored_course_match = CourseMatch.objects.filter(abroadCourse__name=abroad_name, homeCourse__code=homeCode)

        user = User.objects.get(username=request.user)

        hasMatch = user.profile.saved_course_matches.all().filter(abroadCourse__name=abroad_name,
                                                                  homeCourse__code=homeCode)
        if (stored_course_match and hasMatch):
            return HttpResponse(status=409)
        elif (stored_course_match and not hasMatch):
            user.profile.saved_course_matches.add(stored_course_match[0])

            response = {
                'code': 200,
                'message': 'Match lagret i profil',
                'course_match_id': stored_course_match[0].pk
            }
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )

        elif (not stored_course_match and not hasMatch):
            abroad_course = AbroadCourse.objects.get(code=abroadCode, name=abroad_name)
            home_course = HomeCourse.objects.get(code=homeCode)
            course_match = CourseMatch(abroadCourse=abroad_course, homeCourse=home_course)
            course_match.save()
            user.profile.saved_course_matches.add(course_match)

            response = {
                'code': 200,
                'message': 'Match lagret i profil og database',
                'course_match_id': course_match.pk
            }

            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )


@login_required
def save_course_match_id(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        id = request.POST["id"]
        stored_course_match = get_object_or_404(CourseMatch, id=id)
        hasMatch = user.profile.saved_course_matches.all().filter(id=id)
        same_university_as_stored = user.profile.saved_course_matches.all()[
                                        0].abroadCourse.university.name == stored_course_match.abroadCourse.university.name
        if (hasMatch):
            return HttpResponse(status=409)
        elif (not same_university_as_stored):
            return HttpResponse(status=406)
        else:
            user.profile.saved_course_matches.add(stored_course_match)
            return HttpResponse({'code': 200, 'message': 'Match lagret i profil'})


class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'application/application_list.html'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data(**kwargs)
        return context


class ApplicationListAll(UserPassesTestMixin, ListView):
    model = Application
    template_name = 'application/application_list_all.html'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Advisors'])

    def get_queryset(self):
        return Application.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ApplicationListAll, self).get_context_data(**kwargs)
        return context


@login_required
def remove_application(request):
    if request.method == 'POST':
        application_id = request.POST['id']
        Application.objects.get(id=application_id, user=request.user).delete()

        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


def user_is_advisor(user):
    return user.groups.filter(name__in=['Advisors'])


@login_required
@user_passes_test(user_is_advisor)
def edit_status_application(request):
    if request.method == 'POST':
        application_id = request.POST['id']
        change_status_to = request.POST["type"]
        if (change_status_to == "approve"):
            application = Application.objects.get(id=application_id)
            application.status = 'A'
            application.save()
            for course_match in application.course_matches.all():
                cm = CourseMatch.objects.get(id=course_match.pk)
                cm.approved = True
                cm.approval_date = datetime.date.today()
                cm.save()
        elif (change_status_to == "disapprove"):
            application = Application.objects.get(id=application_id)
            application.status = 'D'
            application.save()
            for course_match in application.course_matches.all():
                cm = CourseMatch.objects.get(id=course_match.pk)
                cm.approved = False
                cm.approval_date = None
                cm.save()
        else:
            return HttpResponse({'code': 400, 'message': 'invalid request'})

        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


def save_home_course(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        response_data = {}
        home_course = get_object_or_404(HomeCourse, name=request.POST.get('name'), code=request.POST.get('code'))
        if (user.profile.coursesToTake.filter(code=request.POST.get('code'))):
            response_data["error"] = "Faget finnes allerede i din profil"
        else:
            user.profile.coursesToTake.add(home_course)
            response_data["code"] = request.POST.get('code')
            response_data["name"] = request.POST.get('name')
            response_data["id"] = home_course.pk

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})
