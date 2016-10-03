from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^process/$', views.process, name='process'),
    url(r'^courseMatch/', views.course_match, name='courseMatch'),
    url(r'^process/result/', views.result, name='result')
]
