from django.shortcuts import render, redirect
import requests
import json
from .forms import *
from profiles.models import *
from django.contrib.auth.decorators import login_required


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
            filtered_cases = request.session['result']

        else:
            for case in request.session['result']:
                if case['University'] == university:
                    filtered_cases.append(case)

        return render(request, 'utsida/resultFiltered.html', {'similar_cases': filtered_cases, 'universities': request.session['unique_universities'], 'matches': request.session['matches']})

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
            for case in sorted_full_similar_cases:
                if not case['University'] in unique_unis:
                    unique_unis.append(case['University'])

            request.session['unique_universities'] = unique_unis
            request.session['result'] = sorted_full_similar_cases
            request.session['matches'] = course_wanted_to_be_taken_matches

            return render(request, 'utsida/result.html',
                          {'form': form, 'similar_cases': sorted_full_similar_cases, 'courses_taken': courses_taken, 'matches': course_wanted_to_be_taken_matches, 'universities': unique_unis})



    else:
        form = QueryCaseBaseForm()

    return render(request, 'utsida/process.html', {'form': form})


def courseMatch(request):
    if not request.user.is_authenticated():
        return redirect("login")
    course_matches = CourseMatch.objects.all()
    university_list = University.objects.all()
    context = {"course_match_list": course_matches, "university_list": university_list}
    return render(request, "utsida/courseMatch.html", context)
