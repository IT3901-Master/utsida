from django.conf.urls import url, include
from django.contrib.auth.decorators import user_passes_test

from profiles.forms import MyAuthenticationForm
from profiles.views import ApplicationListView, ApplicationListAll
from . import views
from django.contrib.auth import views as auth_views
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    url(r'register/$', views.register_user, name="register"),
    url(r'update/$', views.update_profile, name="update"),
    url(r'set_institute/$', views.set_institute, name="set_institute"),
    url(r'^login/$', auth_views.login, {'authentication_form': MyAuthenticationForm}, name='login', ),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^change_password/$', views.change_password, name='password_change'),
    url(r'^courses/$', views.saved_courses, name='saved_courses'),
    url(r'^save_courses/$', views.save_courses, name='save_courses'),
    url(r'^save_home_course/$', views.save_home_course, name='save_home_course'),
    url(r'^remove_course/$', views.remove_course, name='remove_course'),
    url(r'^remove_course_match/$', views.remove_course_match, name='remove_course_match'),
    url(r'^remove_all_courses/$', views.remove_all_courses, name='remove_all_courses'),
    url(r'^remove_home_course/$', views.remove_home_course, name='remove_home_course'),
    url(r'^send_approval/$', views.send_applation, name="send_approval"),
    url(r'^save_course_match/$', views.save_course_match, name="save_course_match"),
    url(r'^save_course_match_id/$', views.save_course_match_id, name="save_course_match_id"),
    url(r'^soknader/$', ApplicationListView.as_view(), name='soknader'),
    url(r'^remove_application/$', views.remove_application, name='remove_application'),
    url(r'^soknader/all/$', views.ApplicationListAll.as_view(), name='article-list'),
    url(r'^application/editstatus/$', views.edit_status_application, name='remove_application'),
    url(r'^application/edit/(?P<id>\d+)/$', views.edit_application, name='edit_application'),
    url(r'^abroadCourse/add/$', views.add_abroad_course_to_profile, name='add_abroad_course_to_profile'),

]
