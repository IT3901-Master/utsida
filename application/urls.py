from django.conf.urls import url, include

urlpatterns = [
    url('^$', include("utsida.urls"), name="index"),
]
