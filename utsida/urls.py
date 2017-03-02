from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^process/$', views.process, name='process'),
    url(r'^courseMatch/$', views.course_match_select_continent, name='course_match_select_continent'),
    url(r'^information/$', views.information, name='information'),
    url(r'^process/result/$', views.result, name='result'),
    url(r'^process/result/(?P<university>[_(-,\w ]+)/$', views.result, name='filtered_result'),
    url(r'^courseMatch/(?P<university>\d+)/$', views.courseMatch, name='courseMatch'),
    url(r'^courseMatch/university/$', views.courseMatch, name='courseMatch'),
    url(r'^courseMatch/add/$', views.add_course_match, name='add_course_match'),
    url(r'^courseMatch/delete/$', views.delete_course_match, name='add_course_match'),
    url(r'^courseMatch/update/(?P<id>\d+)/$', views.update_course_match, name="update_course_match"),
    url(r'^courseMatch/countrySelect/$', views.course_match_select_country, name='course_match_select_continent'),
    url(r'^courseMatch/universitySelect/$', views.course_match_select_university, name='course_match_select_continent'),
    url(r'^abroadCourse/add/$', views.add_abroad_course, name='add_abroad_course_to_profile'),
    url(r'^api/countries/$', views.get_countries),
]
