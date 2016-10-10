import random as r
import json

rating = [1, 2, 3, 4, 5]
period = range(2010, 2016)
countries = []
faculties = []
languages = []
universities = []
subjects = ["IT2805", "CS1010", "TECH8989", "PC8911", "CS7810", "DATA0987"]
file = []


def generate_cases():

    counter = 1

    for i in range(0, 5):
        case = {}
        case["pk"] = counter
        case["model"] = "utsida.case"
        case["fields"] = {}
        case["fields"]["homeInstitute"] = r.choice(faculties)
        case["fields"]["continent"] = "North America"
        case["fields"]["country"] = r.choice(countries)
        case["fields"]["university"] = r.choice(universities)
        case["fields"]["studyPeriod"] = r.choice(period)
        case["fields"]["language"] = r.choice(languages)
        case["fields"]["academicQualityRating"] = r.choice(rating)
        case["fields"]["socialQualityRating"] = r.choice(rating)
        case["fields"]["language"] = r.choice(languages)
        case["fields"]["subjects"] = [r.choice(subjects), r.choice(subjects), r.choice(subjects), r.choice(subjects)]
        file.append(case)


def fill_faculties():
    file = open("attributes/faculties.txt", "r")
    for line in file:
        faculties.append(line.rstrip('\n'))
    file.close()


def fill_universities():
    file = open("attributes/universities.txt", "r")
    for line in file:
        universities.append(line.rstrip('\n'))
    file.close()


def fill_languages():
    file = open("attributes/languages.txt", "r")
    for line in file:
        languages.append(line.rstrip('\n'))
    file.close()


def fill_countries():
    file = open("attributes/countries.txt", "r")
    for line in file:
        countries.append(line.rstrip('\n'))
    file.close()


def get_data():
    fill_faculties()
    fill_countries()
    fill_languages()
    fill_universities()


def to_json():
    json_data = json.dumps(file)
    target = open("../../utsida/fixtures/cases.json", "w")
    target.write(json_data)
    target.close()


if __name__ == "__main__":
    get_data()
    generate_cases()
    to_json()
