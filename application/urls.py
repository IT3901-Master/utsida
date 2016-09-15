from django.conf.urls import url, include
from . import views
from django.contrib import admin

urlpatterns = [
    url('^$', views.IndexView.as_view(), name="index"),
]
