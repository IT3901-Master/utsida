from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .models import Institute
import json


def index(request):
    return render(request, "utsida/index.html")


def process(request):
    institute_list = Institute.objects.all()
    context = {"institute_list" : institute_list}
    return render(request, "utsida/process.html", context)

