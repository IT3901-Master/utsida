import re

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
import json
from .forms import *
from profiles.models import *
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from fuzzywuzzy import fuzz


def index(request):
    if not request.user.is_authenticated():
        return redirect("login")
    return render(request, "utsida/index.html")


def process(request):
    if not request.user.is_authenticated():
        return redirect("login")
    form = QueryCaseBaseForm()
    return render(request, "utsida/process.html", {"form": form})


def result(request, university=None):
    if not request.user.is_authenticated():
        return redirect("login")
    if university:
        filtered_cases = []

        if university == "all":
            filtered_cases = request.session['result'][:9]

        else:
            for case in request.session['result']:
                if case['University'] == university:
                    filtered_cases.append(case)

        return render(request, 'utsida/result.html', {'similar_cases': filtered_cases, 'universities': request.session['unique_universities'], 'matches': request.session['matches'], 'show_loader': False})

    if request.method == 'POST':
        form = QueryCaseBaseForm(request.POST)
        user_profile = User.objects.get(username=request.user).profile
        institute = user_profile.institute.__str__()
        courses_taken = []
        courses_taken_object = request.user.profile.coursesToTake.all()

        for course in courses_taken_object:
            courses_taken.append(str(course))

        if form.is_valid():

            payload = json.dumps({
                "Institute": institute,
                "Continent": form.data["continent"],
                "Country": form.data["country"],
                "University": form.data["university"],
                "Language": form.data["language"],
                "StudyPeriod": datetime.date.today().year,
                "AcademicQuality": form.data["academicQualityRating"],
                "SocialQuality": form.data["socialQualityRating"],
            })
            headers = {
                'content-type': 'application/json'
            }

            r = requests.post("http://localhost:8080/retrieval?casebase=main_case_base&concept%20name=Trip",
                              data=payload,
                              headers=headers
                              ).json()["similarCases"]

            full_similar_cases = []

            for key, value in r.items():
                full_case = requests.get("http://localhost:8080/case?caseID=" + key).json()["case"]
                full_case["Subjects"] = full_case["Subjects"].split('!')
                full_case["Similarity"] = "%.3f" % value
                full_similar_cases.append(full_case)

            sorted_full_similar_cases = sorted(full_similar_cases, key=lambda k: k['Similarity'], reverse=True)

            courses = request.user.profile.coursesToTake.all()

            course_wanted_to_be_taken_matches = {}

            for course in courses:
                results = CourseMatch.objects.filter(homeCourse=course)
                if results:
                    for result in results:
                        course_wanted_to_be_taken_matches[str(result.abroadCourse)] = course.code

            unique_unis = []
            for case in sorted_full_similar_cases[:9]:
                if not case['University'] in unique_unis:
                    unique_unis.append(case['University'])

            '''
            uni_counter = 0
            for uni in unique_unis:
                if fuzz.ratio(uni, unique_unis[uni_c



                ounter+1]) > 90:
                    del unique_unis[unique_unis.index(uni)]
                uni_counter += 1
            '''

            request.session['unique_universities'] = unique_unis
            request.session['result'] = sorted_full_similar_cases
            request.session['matches'] = course_wanted_to_be_taken_matches

            return render(request, 'utsida/result.html',
                          {'form': form, 'similar_cases': sorted_full_similar_cases[:9], 'courses_taken': courses_taken, 'matches': course_wanted_to_be_taken_matches, 'universities': unique_unis, 'show_loader': True})



    else:
        form = QueryCaseBaseForm()

    return render(request, 'utsida/process.html', {'form': form})


@login_required
def courseMatch(request):
    university = request.POST["university"]
    #Remove the paranthesis, example: (103)
    university = re.sub(r'\([^)]*\)', '', university)[:-1]
    add_form = CourseMatchForm()
    add_form.fields["abroadCourse"].queryset = AbroadCourse.objects.filter(university__name=university)
    course_matches = CourseMatch.objects.all().filter(abroadCourse__university__name=university)
    context = {"course_match_list": course_matches,"university_name":university, "add_form":add_form}
    return render(request, "utsida/courseMatch.html", context)



@login_required
@permission_required('utsida.can_update_course_match')
@transaction.atomic
def update_course_match(request, id):
    instance = get_object_or_404(CourseMatch, id=id)
    if request.method == "POST":
        form = CourseMatchForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            university = form.cleaned_data["abroadCourse"].university
            add_form = CourseMatchForm()
            add_form.fields["abroadCourse"].queryset = AbroadCourse.objects.filter(university__name=university)
            course_matches = CourseMatch.objects.all().filter(abroadCourse__university__name=university)
            context = {"course_match_list": course_matches, "university_name": university, "add_form": add_form}
            messages.success(request, "Fag kobling ble endret")
            return render(request, "utsida/courseMatch.html", context)
        else:
            return HttpResponse({'code': 500, 'message': 'skjema var ikke gyldig'})
    else:
        #form = CourseMatchForm(initial={"abroadCourse": instance.abroadCourse})
        form = CourseMatchForm(instance=instance)
        return render(request,"utsida/update_course_match.html", {"form":form,"id":id})

@permission_required('utsida.can_add_course_match')
def add_course_match(request):
    if request.POST:
        form = CourseMatchForm(request.POST)
        if form.is_valid():
            form.save()
            university = form.cleaned_data["abroadCourse"].university
            add_form = CourseMatchForm()
            add_form.fields["abroadCourse"].queryset = AbroadCourse.objects.filter(university__name=university)
            course_matches = CourseMatch.objects.all().filter(abroadCourse__university__name=university)
            context = {"course_match_list": course_matches, "university_name": university, "add_form": add_form}
            messages.success(request,"Ny fag-kobling ble lagt til")
            return render(request, "utsida/courseMatch.html", context)
        else:
            messages.error(request, "Endre feilene under")
            return HttpResponse({'code': 500, 'message': 'Du må fylle inn alle feltene'})



@login_required
def course_match_select_university(request):
    if not request.user.is_authenticated():
        return redirect("login")

    university_list = University.objects.all()
    for university in university_list:
        university.count = len(CourseMatch.objects.all().filter(abroadCourse__university__name=university.name))

    context = {"university_list":university_list}
    return render(request, "utsida/course_match_university_select.html",context)

@permission_required('utsida.can_delete_course_match')
@login_required
def delete_course_match(request):
    if request.method == 'POST':
        course_match_id = request.POST['id']
        CourseMatch.objects.get(id=course_match_id).delete()
        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})