from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
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


def get_user_profile(request,username):
    user = User.objects.get(username=username)
    print(user.first_name)
    return render(request, 'utsida/user_profile.html', {"user": user})