from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^process/$', views.process, name='process'),
    url(r'^courseMatch/$', views.course_match_select_university, name='course_match_select_university'),
    url(r'^process/result/$', views.result, name='result'),
    url(r'^process/result/(?P<university>[\w ]+)/$', views.result, name='filtered_result'),
    url(r'^courseMatch/university/$', views.courseMatch, name='courseMatch'),
]
