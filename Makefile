
load:
	python3 manage.py loaddata continents.json
	python3 manage.py loaddata countries.json
	python3 manage.py loaddata faculties.json
	python3 manage.py loaddata institutes.json
	python3 manage.py loaddata homeCourses.json
	python3 manage.py loaddata languages.json
	python3 manage.py loaddata universities.json
	python3 manage.py loaddata abroad_courses1
	python3 manage.py loaddata abroad_courses2
	python3 manage.py loaddata abroad_courses3
	python3 manage.py loaddata abroad_courses4
	python3 manage.py loaddata abroad_courses5
	python3 manage.py loaddata course_matches1
	python3 manage.py loaddata course_matches2
	python3 manage.py loaddata course_matches3
	python3 manage.py loaddata course_matches4
	python3 manage.py loaddata course_matches5


makemigrations:
	python3 manage.py makemigrations utsida
	python3 manage.py makemigrations profiles

migrate:
	python3 manage.py migrate

run: 
	python3 manage.py runserver
super:
	python3 manage.py createsuperuser
