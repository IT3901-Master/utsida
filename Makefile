
#loading startup data for the application

load:
	make loadstart
	make loadcourse

loadstart:
	python3 manage.py loaddata start_data/continents.json
	python3 manage.py loaddata start_data/countries.json
	python3 manage.py loaddata start_data/faculties.json
	python3 manage.py loaddata start_data/institutes.json
	python3 manage.py loaddata start_data/homeCourses.json
	python3 manage.py loaddata start_data/languages.json
	python3 manage.py loaddata start_data/universities.json

loadcourse:
	python3 manage.py loaddata course_data/oceania/c0.json
	python3 manage.py loaddata course_data/oceania/c1.json
	python3 manage.py loaddata course_data/oceania/c2.json
	python3 manage.py loaddata course_data/oceania/c3.json
	python3 manage.py loaddata course_data/oceania/c4.json
	python3 manage.py loaddata course_data/oceania/c5.json
	python3 manage.py loaddata course_data/oceania/c6.json
	python3 manage.py loaddata course_data/oceania/c7.json
	python3 manage.py loaddata course_data/oceania/c8.json
	python3 manage.py loaddata course_data/oceania/cm0.json
	python3 manage.py loaddata course_data/oceania/cm1.json
	python3 manage.py loaddata course_data/oceania/cm2.json
	python3 manage.py loaddata course_data/oceania/cm3.json
	python3 manage.py loaddata course_data/oceania/cm4.json
	python3 manage.py loaddata course_data/oceania/cm5.json
	python3 manage.py loaddata course_data/oceania/cm6.json
	python3 manage.py loaddata course_data/oceania/cm7.json
	python3 manage.py loaddata course_data/oceania/cm8.json
	python3 manage.py loaddata course_data/america/c0.json
	python3 manage.py loaddata course_data/america/cm0.json
	python3 manage.py loaddata course_data/america/c1.json
	python3 manage.py loaddata course_data/america/cm1.json



makemigrations:
	python3 manage.py makemigrations utsida --settings=config.settings.local
	python3 manage.py makemigrations profiles --settings=config.settings.local

migrate:
	python3 manage.py migrate --settings=config.settings.local

lrun:
	python3 manage.py runserver --settings=config.settings.local
	
prun:
	python3 manage.py runserver --settings=config.settings.production

super:
	python3 manage.py createsuperuser
