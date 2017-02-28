import urllib.request as urllib
from html.parser import HTMLParser
import json
import glob
import time


data_list = []
COUNTRY_COUNT = {}
COUNTRY_CODE_DICT = {}


class Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

    def destroy(self):
        del self

    def handle_data(self, data):
        global data_list
        data_list.append(data)


def get_html():
    url = "Internasjonal Seksjon.html"
    result = urllib.urlopen(url)
    return result.read().decode("utf-8").replace('\r\n', ' ')


def parse_html():
    for i in range(0, len(data_list)):
        element = data_list[i]
        if element == "Land:":
            next_element = str(data_list[i+1]).strip().replace('\n', '').replace(' ', '')
            
            try:
                COUNTRY_COUNT [next_element] += 1
            except KeyError:
                COUNTRY_COUNT [next_element] = 1

    return COUNTRY_COUNT 


def run(s):
    global data_list
    html = open(s, 'r')
    P = Parser()
    P.feed(html.read())
    html.close()
    parse_html()
    P.destroy()
    P.close()
    data_list = []
    

def start():
    data_list = []
    file_list = glob.glob("../retrieved_html_files/*.html")
    counter = 0
    stopper = 0
    for file in file_list:
        print("Starting: " + str(file))
        run(file)
        if stopper >= 100000:
            return

        counter += 1
        stopper += 1
        print("Finished: " + str(file) + " (" + str(counter) + '/' + "10857)")


def make_js_file():
    counter = 0

    with open('country_codes.js', 'w') as target:
        target.write("var country_code_data = {")
        for k, v in COUNTRY_COUNT.items():

            if k == "Brazil":
                k = "Brasil"
            elif k == "Sweden":
                k = "Sverige"
            elif k == "Germany":
                k = "Tyskland"
            elif k == "albania":
                k = "Albania"
            elif k == "Columbia":
                k = "Colombia"
            elif k == "SørAfrika":
                k = "Sør Afrika"
            elif k == "TheNetherlands":
                k = "Nederland"
            elif k == "NewZealand":
                k = "New Zealand"
            elif k == "CostaRica":
                k = "Costa Rica"

            try:
                code = COUNTRY_CODE_DICT[k]

                if counter == len(COUNTRY_COUNT)-1:
                    target.write("'" + COUNTRY_CODE_DICT[k] + "': " + str(v))
                    target.write('}')
                else:
                    target.write("'" + COUNTRY_CODE_DICT[k] + "': " + str(v) + ',')
                    counter += 1

            except KeyError as err:
                print("ERROR: ", err)
                time.sleep(1)
                counter += 1
                continue

    target.close()


def make_country_code_dict():
    with open('377.csv', 'r', encoding='latin-1') as data:
        for line in data:
            code = line.split(';')[0]
            name = line.split(';')[2].strip().replace('"', '')

            COUNTRY_CODE_DICT[name] = code

    for k, v in COUNTRY_CODE_DICT.items():
        print(k, ': ', v)

    data.close()


def print_cases():
    for k, v in COUNTRY_COUNT.items():
        print(k, ': ', v)


if __name__ == "__main__":
    make_country_code_dict()
    start()
    #print_cases()
    make_js_file()
