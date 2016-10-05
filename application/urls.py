from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include("profiles.urls"), name='profiles'),
    url('^', include("utsida.urls"), name="index"),
<<<<<<< HEAD
=======

>>>>>>> e33d957817159d596fc80a4193f71c66b338a6f0
]
