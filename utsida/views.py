import datetime
from django.core import serializers
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
import json
from .forms import *
from profiles.models import *
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.validators import *


def index(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = User.objects.get(username=request.user)
    if (user.groups.filter(name='Advisors').exists()):
        return advisors(request)
    else:
        return render(request, "utsida/index.html")


def information(request):
    return render(request, 'utsida/information.html')


@login_required
def advisors(request):
    application_data = {
        'count': Application.objects.all().count(),
        'num_approved': Application.objects.all().filter(status='A').count(),
        'num_pending': Application.objects.all().filter(status='P').count(),
        'num_rejected': Application.objects.all().filter(status='D').count()
    }

    course_match_data = {
        'count': str(CourseMatch.objects.all().count())
    }

    return render(
        request,
        'utsida/advisors.html',
        {
            'application_data': application_data,
            'course_match_data': course_match_data
        }
    )


@login_required
def process(request):
    if not request.user.is_authenticated():
        return redirect("login")
    form = QueryCaseBaseForm()
    return render(request, "utsida/process.html", {"form": form})


@login_required
def result(request, university=None):
    if not request.user.is_authenticated():
        return redirect("login")

    # If the request has a university parameter, return a every case with that university
    if university:
        filtered_cases = []
        filter = True

        if university == "all":
            filtered_cases = request.session['result'][:9]
            new_filtered_cases = []
            unis = []

            for case in filtered_cases:
                university = case['content']['University']

                if university not in unis:
                    new_filtered_cases.append(case)
                    unis.append(university)

            filter = False

            return render(request, 'utsida/result.html',
                          {'similar_cases': new_filtered_cases[:6],
                           'universities': request.session['unique_universities'],
                           'matches': request.session['matches'], 'filter': filter})

        else:
            for case in request.session['result']:
                if 'University' in case['content'] and case['content']['University'] == university:
                    filtered_cases.append(case)

            return render(request, 'utsida/result.html',
                          {'similar_cases': filtered_cases[:9], 'universities': request.session['unique_universities'],
                           'matches': request.session['matches'], 'filter': filter})

    # Else the request is a normal query
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
                "StudyPeriod": int(datetime.date.today().year),
                "AcademicQuality": form.data["academicQualityRating"],
                "SocialQuality": form.data["socialQualityRating"],
                "ResidentialQuality": form.data["residentialQualityRating"],
                "ReceptionQuality": form.data["receptionQualityRating"],
            })
            headers = {
                'content-type': 'application/json'
            }

            r = requests.post("http://localhost:8080/retrieval?casebase=main_case_base&concept%20name=Trip",
                              data=payload,
                              headers=headers
                              ).json()["similarCases"]

            for case in r:
                if 'Language' in case['content']:
                    case['content']['Language'] = case['content']['Language'].split(';')
                case['content']['Subjects'] = case['content']['Subjects'].split('!')
                case['similarity'] = "%.3f" % case['similarity']

            # Sorting the case list based on similarity
            sorted_similar_cases = sorted(r, key=lambda k: k['similarity'], reverse=True)

            courses = request.user.profile.coursesToTake.all()

            course_wanted_to_be_taken_matches = {}

            for course in courses:
                results = CourseMatch.objects.filter(homeCourse=course)
                if results:
                    for result in results:
                        course_wanted_to_be_taken_matches[str(result.abroadCourse)] = course.code + ' ' + course.name

            unique_unis = []
            unique_sorted_similar_cases = []
            for case in sorted_similar_cases[:9]:
                if 'University' in case['content'] and not case['content']['University'] in unique_unis:
                    unique_sorted_similar_cases.append(case)
                    unique_unis.append(case['content']['University'])

            request.session['unique_universities'] = unique_unis
            request.session['result'] = sorted_similar_cases
            request.session['matches'] = course_wanted_to_be_taken_matches

            rating_list = {}

            for case in sorted_similar_cases:
                uni = case['content']['University']
                if uni not in rating_list:
                    rating_list[uni] = {
                        'social_quality': int(case['content']['SocialQuality']),
                        'academic_quality': int(case['content']['AcademicQuality']),
                        'residential_quality': int(case['content']['ResidentialQuality']),
                        'reception_quality': int(case['content']['ReceptionQuality']),
                        'count': 1
                    }

                elif case['content']['University'] in rating_list:
                    rating_list[uni]['social_quality'] += int(case['content']['SocialQuality'])
                    rating_list[uni]['academic_quality'] += int(case['content']['AcademicQuality'])
                    rating_list[uni]['residential_quality'] += int(case['content']['ResidentialQuality'])
                    rating_list[uni]['reception_quality'] += int(case['content']['ReceptionQuality'])
                    rating_list[uni]['count'] += 1

            for uni, values in rating_list.items():
                values['social_quality'] = round(int(values['social_quality']) / int(values['count']))
                values['academic_quality'] = round(int(values['academic_quality']) / int(values['count']))
                values['residential_quality'] = round(int(values['residential_quality']) / int(values['count']))
                values['reception_quality'] = round(int(values['reception_quality']) / int(values['count']))

            for case in unique_sorted_similar_cases[:6]:
                for rating in rating_list:
                    if rating == case['content']['University']:
                        case['university_ratings'] = rating_list[rating]

            return render(request, 'utsida/result.html',
                          {'form': form, 'similar_cases': unique_sorted_similar_cases[:6],
                           'courses_taken': courses_taken,
                           'matches': course_wanted_to_be_taken_matches, 'universities': unique_unis,
                           'rating_list': rating_list, 'filter': False})

    else:
        form = QueryCaseBaseForm()

    return render(request, 'utsida/process.html', {'form': form})


@login_required
def courseMatch(request):
    university = request.POST.get("university")
    # Remove the paranthesis, example: (103)
    university = re.sub(r'\([^)]*\)', '', university)[:-1]
    full_university = get_object_or_404(University, name=university)
    add_form = CourseMatchForm()
    add_form.fields["abroadCourse"].queryset = AbroadCourse.objects.filter(university__name=university)
    course_matches = CourseMatch.objects.all().filter(abroadCourse__university__name=university)
    abroad_course_form = abroadCourseForm()
    context = {"course_match_list": course_matches, "university_name": university, "university": full_university,
               "add_form": add_form, "add_abroad_form": abroad_course_form}
    return render(request, "utsida/courseMatch.html", context)


@login_required
@permission_required('utsida.can_update_course_match')
@transaction.atomic
def update_course_match(request, id):
    instance = get_object_or_404(CourseMatch, id=id)
    if request.method == "POST":
        form = CourseMatchForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            university = form.cleaned_data["abroadCourse"].university
            add_form = CourseMatchForm()
            add_form.fields["abroadCourse"].queryset = AbroadCourse.objects.filter(university__name=university)
            course_matches = CourseMatch.objects.all().filter(abroadCourse__university__name=university)
            abroad_course_form = abroadCourseForm()
            context = {"course_match_list": course_matches, "university_name": university, "add_form": add_form,
                       "add_abroad_form": abroad_course_form}
            messages.success(request, "Fag kobling ble endret")
            return render(request, "utsida/courseMatch.html", context)
        else:
            return HttpResponse({'code': 500, 'message': 'skjema var ikke gyldig'})
    else:
        form = CourseMatchForm(instance=instance)
        return render(request, "utsida/update_course_match.html", {"form": form, "id": id})


@permission_required('utsida.can_add_course_match')
def add_course_match(request):
    if request.POST:
        home_course = get_object_or_404(HomeCourse, code=request.POST['homeCourse'].split('-')[0].strip())
        abroad_course = get_object_or_404(AbroadCourse, code=request.POST['abroadCourse'].split('-')[0].strip(),
                                          university__name=request.POST['university'])
        approved = False
        if (request.POST['approved'] == "on"):
            approved = True
            approver = User.objects.get(username=request.user)
        else:
            approver = None
        approval_date = request.POST['approval_date']
        course_match = CourseMatch(homeCourse=home_course, abroadCourse=abroad_course, approved=approved,
                                   approval_date=approval_date, reviewer=approver)
        course_match.save()
        university = abroad_course.university
        add_form = CourseMatchForm()
        add_form.fields["abroadCourse"].queryset = AbroadCourse.objects.filter(university__name=university)
        course_matches = CourseMatch.objects.all().filter(abroadCourse__university__name=university)
        abroad_course_form = abroadCourseForm()
        context = {"course_match_list": course_matches, "university_name": university, "university": university,
                   "add_form": add_form, "add_abroad_form": abroad_course_form}
        messages.success(request, "Ny fag-kobling ble lagt til")
        return render(request, "utsida/courseMatch.html", context)
    else:
        messages.error(request, "Endre feilene under")
        return HttpResponse({'code': 500, 'message': 'Du må fylle inn alle feltene'})


@login_required
def add_abroad_course(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)

        abroad_course = AbroadCourse(university=get_object_or_404(University, name=request.POST['university']),
                                     name=request.POST['name'], code=request.POST['code'],
                                     description_url=request.POST['description_url'],
                                     study_points=request.POST['study_points'])
        abroad_course.save()
        university = abroad_course.university
        add_form = CourseMatchForm()
        add_form.fields["abroadCourse"].queryset = AbroadCourse.objects.filter(university__name=university)
        course_matches = CourseMatch.objects.all().filter(abroadCourse__university__name=university)
        context = {"course_match_list": course_matches, "university_name": university, "add_form": add_form}
        messages.success(request, "Nytt fag ble lagt til")
        return render(request, "utsida/courseMatch.html", context)


@login_required
def course_match_select_university(request):
    country = request.POST.get("country")
    university_list = University.objects.all().filter(country__name=country)

    for university in university_list:
        university.count = len(
            CourseMatch.objects.all().filter(abroadCourse__university__name=university.name, approved=True))

    response_data = []

    for university in university_list:
        data = {"name": university.name, "count": university.count}
        response_data.append(data)

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def course_match_select_continent(request):
    unique_continents = []
    university_list = University.objects.all()

    country_list = []
    for university in university_list:
        if not university.country.name in country_list:
            country_list.append(university.country.name)

    for university in university_list:
        if not university.country.continent in unique_continents:
            unique_continents.append(university.country.continent)

    for university in university_list:
        university.count = len(
            CourseMatch.objects.all().filter(abroadCourse__university__name=university.name, approved=True))


    context = {"continent_list": unique_continents, "university_list": university_list, "country_list": country_list}
    return render(request, "utsida/course_match_continent_select.html", context)


@login_required
def course_match_select_country(request):
    country_list = []
    continent = request.POST.get("continent")
    universities = University.objects.all()
    university_list = []
    for university in universities:
        if university.country.continent.name == continent:
            if not university.name in university_list:
                university_list.append(university)
            if not university.country.name in country_list:
                country_list.append(university.country.name)


    for university in university_list:
        university.count = len(
            CourseMatch.objects.all().filter(abroadCourse__university__name=university.name, approved=True))

    university_data = []

    for university in university_list:
        data = {"name": university.name, "count": university.count}
        university_data.append(data)


    return HttpResponse(
        json.dumps({"country_list":country_list,"university_list":university_data}),
        content_type="application/json"
    )


@permission_required('utsida.can_delete_course_match')
@login_required
def delete_course_match(request):
    if request.method == 'POST':
        course_match_id = request.POST['id']
        CourseMatch.objects.get(id=course_match_id).delete()
        return HttpResponse({'code': 200, 'message': 'OK'})
    else:
        return HttpResponse({'code': 500, 'message': 'request is not a post request'})


def get_countries(request):
    continent = request.POST.get('continent')
    countries = Country.objects.all().filter(continent=continent)
    response = serializers.serialize("json", countries)

    return HttpResponse(response, content_type="application/json")
