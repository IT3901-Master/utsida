
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import *
from .forms import *


def index(request):
    return render(request, "utsida/index.html")


def process(request):
    form = QueryCaseBaseForm()
    return render(request, "utsida/process.html", {"form": form})


def result(request):
    if request.method == 'POST':
        form = QueryCaseBaseForm(request.POST)
        if form.is_valid():
            return render(request, 'utsida/result.html', {'form': form})
    else:
        form = QueryCaseBaseForm()

    return render(request, 'utsida/process.html', {'form': form})

def courseMatch(request):
    if request.user.is_authenticated():
        course_matches = CourseMatch.objects.all()
        context = {"course_match_list": course_matches}
    else:
        context = {}
    return render(request,"utsida/courseMatch.html",context)
