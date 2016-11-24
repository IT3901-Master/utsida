
load:
	python3 manage.py loaddata continents.json
	python3 manage.py loaddata countries.json
	python3 manage.py loaddata faculties.json
	python3 manage.py loaddata institutes.json
	python3 manage.py loaddata homeCourses.json
	python3 manage.py loaddata languages.json
	python3 manage.py loaddata universities.json
	python3 manage.py loaddata abroad_courses0
	python3 manage.py loaddata abroad_courses1
	python3 manage.py loaddata abroad_courses2
	python3 manage.py loaddata course_matches0
	python3 manage.py loaddata course_matches1
	python3 manage.py loaddata course_matches2



makemigrations:
	python3 manage.py makemigrations utsida
	python3 manage.py makemigrations profiles

migrate:
	python3 manage.py migrate

run: 
	python3 manage.py runserver
super:
	python3 manage.py createsuperuser
