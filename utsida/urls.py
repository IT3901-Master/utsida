from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
    url(r'^process/', views.process, name="process"),
    url(r'^courseMatch/', views.courseMatch, name="courseMatch"),
    url(r'^process/query/', views.query, name="query"),
]
