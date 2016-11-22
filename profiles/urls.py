from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    url(r'user/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name="profile"),
    url(r'register/$', views.register_user, name="register"),
    url(r'update/$', views.update_profile, name="update"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^change_password/$', views.change_password, name='password_change'),
    url(r'^courses/$', views.saved_courses, name='saved_courses'),
    url(r'^save_courses/$', views.save_courses, name='save_courses'),
    url(r'^remove_course/$', views.remove_course, name='remove_course'),
    url(r'^remove_all_courses/$', views.remove_all_courses, name='remove_all_courses'),
]
