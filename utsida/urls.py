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
    url(r'^courseMatch/(?P<university>\d+)/$', views.courseMatch, name='courseMatch'),
    url(r'^courseMatch/university/$', views.courseMatch, name='courseMatch'),
    url(r'^courseMatch/add/$', views.add_update_course_match, name='add_course_match'),
    url(r'^courseMatch/update/(?P<pk>\d+)/$', views.add_update_course_match, name="update_course_match")
]