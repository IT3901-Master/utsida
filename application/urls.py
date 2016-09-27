from django.conf.urls import url, include
from . import views
from django.contrib import admin

urlpatterns = [
    url('^$', include("utsida/urls"), name="index"),
]
