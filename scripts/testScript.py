#template script file to use for future reference


import os, sys

proj_path = "/Users/trulsmp/Documents/master/utsida"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utsida.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from utsida.models import *

faculty = Faculty(name="Fakultet for informasjonsteknologi, matematikk og elektroteknikk", acronym="IME")
institute = Institute(name="Institutt for datateknikk og informasjonsvitenskap",acronym="IDI",faculty=faculty)

faculty.save()
institute.save()
