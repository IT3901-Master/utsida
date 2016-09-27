from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic


def index(request):
    return render(request, "utsida/index.html")


def process(request):
    return render(request, "utsida/process.html")

