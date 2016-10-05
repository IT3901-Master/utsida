from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'user/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name="profile"),
    url(r'register/$', views.register_user, name="register"),
    url(r'update/$', views.update_profile, name="update"),
    url(r'register_success/$', views.register_success, name="register_success"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
