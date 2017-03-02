import urllib.request as urllib
from html.parser import HTMLParser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import glob
from titlecase import titlecase
import re
import time
import math

data_list = []
star_list = []

cases = []


class Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

    def destroy(self):
        del self

    def handle_data(self, data):
        global data_list
        data_list.append(data)

    def handle_starttag(self, tag, attrs):
        if attrs == [('class', 'fa fa-star-o'), ('aria-hidden', 'true')] or attrs == [('class', 'fa fa-star'), ('aria-hidden', 'true')] or attrs == [('class', 'fa fa-star')] or attrs == [('class', 'fa fa-star-o')]:
            star_list.append(attrs)


def get_html():
    url = "Internasjonal Seksjon.html"
    result = urllib.urlopen(url)
    return result.read().decode("utf-8").replace('\r\n', ' ')


def parse_html():
    data_object = {}
    for i in range(0, len(data_list)):
        element = data_list[i]
        if element == "Hvilke faktorer var avgjørende for deg for å dra til det valgte landet og studiestedet?":
            next_element = data_list[i+4]
            #print(data_list)
            data_object['text'] = next_element.strip().replace('\n', '')

        data_object["academic_quality"] = get_rating("academic")
        data_object["special_competence"] = get_rating("special")
        data_object["cultural_experiences"] = get_rating("cultural")
        data_object["new_friends"] = get_rating("friends")
        data_object["new_impulses"] = get_rating("impulses")
        data_object["job_plans"] = get_rating("job")
        

    return data_object


def get_rating(s):

    if s == "academic":
        return calculate_stars(1, 6)

    elif s == "special":
        return calculate_stars(6, 11)

    elif s == "cultural":
        return calculate_stars(11, 16)

    elif s == "friends":
        return calculate_stars(16, 21)

    elif s == "impulses":
        return calculate_stars(21, 26)

    elif s == "job":
        return calculate_stars(26, 31)

    else:
        return None


def calculate_stars(start, end):
    temp = []
    counter = 0

    for i in range(start, end):
        temp.append(star_list[i])

    for row in temp:
        if row[0][1] == "fa fa-star":
            counter += 1

    return counter


def calculate():
    impulses = 0
    cultural = 0
    academic = 0
    friends = 0
    jobb = 0
    special = 0

    for case in cases:
        impulses += case['new_impulses']
        cultural += case['cultural_experiences']
        academic += case['academic_quality']
        friends += case['new_friends']
        jobb += case['job_plans']
        special += case['special_competence']

    impulses = impulses / 10857
    cultural = cultural / 10857
    academic = academic / 10857
    friends = friends / 10857
    jobb = jobb / 10857
    special = special / 10857

    print("New impulses: ", impulses, "/5")
    print("Cultural experiences: ", cultural, "/5")
    print("Academic quality: ", academic, "/5")
    print("New friends: ", friends, "/5")
    print("Job plans: ", jobb, "/5")
    print("Special competence: ", special, "/5")


def run(s):
    global data_list
    global star_list
    html = open(s, 'r')
    P = Parser()
    P.feed(html.read())
    html.close()
    obj = parse_html()
    P.destroy()
    P.close()
    data_list = []
    star_list = []
    return obj


def print_cases():
    for case in cases:
        for k, v in case.items():
            print(k + ':', v)
        print('-'*100)


def start():
    data_list = []
    star_list = []
    file_list = glob.glob("../retrieved_html_files/*.html")
    counter = 0
    stopper = 0
    for file in file_list:
        print("Starting: " + str(file))
        case = run(file)
        case['url'] = "https://www.ntnu.no/studier/studier_i_utlandet/rapport/report.php?recordid=" + file.split('/')[1].split('file')[1].split('html')[0]
        if stopper >= 100000:
            return
        cases.append(case) 
        counter += 1
        stopper += 1
        print("Finished: " + str(file) + " (" + str(counter) + '/' + "10857)")

def make_json():
    with open('motivation.json', 'w', encoding='utf-8') as target:
        json_file = json.dumps(cases, ensure_ascii=False)
        target.write(json_file)


if __name__ == "__main__":
    start()
    #calculate()
    #print(cases)
    make_json()
    #print_cases()
    
