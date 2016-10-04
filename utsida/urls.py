from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', views.index, name="index"),
    url(r'^process/', views.process, name="process"),
    url(r'^courseMatch/', views.courseMatch, name="courseMatch"),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile)
]
