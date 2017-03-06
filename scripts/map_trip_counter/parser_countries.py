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
        #print("Starting: " + str(file))
        run(file)
        if stopper >= 100000:
            return

        counter += 1
        stopper += 1
        #print("Finished: " + str(file) + " (" + str(counter) + '/' + "10857)")


def make_js_file():
    counter = 0

    with open('country_codes.js', 'w') as target:
        target.write("var country_code_data = {")
        for k, v in COUNTRY_COUNT.items():

            try:
                code = COUNTRY_CODE_DICT[k]

                if counter == len(COUNTRY_COUNT)-1:
                    target.write("'" + code + "': " + str(v))
                    target.write('};')
                else:
                    target.write("'" + code + "': " + str(v) + ',')
                    counter += 1

            except KeyError as err:
                print('ERROR: ', err)
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


def fix_dictionary():
        COUNTRY_COUNT["De Forente Arabiske Emirater"] = COUNTRY_COUNT.pop("Forentearabiskeemirater")
        COUNTRY_COUNT["New Zealand"] = COUNTRY_COUNT.pop("NewZealand")
        COUNTRY_COUNT["Tyskland"] = COUNTRY_COUNT["Tyskland"] + COUNTRY_COUNT.pop("Germany")
        COUNTRY_COUNT["Østerrike"] = COUNTRY_COUNT.pop("Ã˜sterrike")
        COUNTRY_COUNT["Sør Afrika"] = COUNTRY_COUNT.pop("SÃ¸rAfrika")
        COUNTRY_COUNT["Sør Afrika"] = COUNTRY_COUNT.pop("SørAfrika")
        COUNTRY_COUNT["Den Dominikanske Republikk"] = COUNTRY_COUNT.pop("DenDominikanskerepublikk")
        COUNTRY_COUNT["Albania"] = COUNTRY_COUNT.pop("albania")
        COUNTRY_COUNT["Reunion"] = COUNTRY_COUNT.pop("LaRéunion")
        COUNTRY_COUNT["Costa Rica"] = COUNTRY_COUNT.pop("CostaRica")
        COUNTRY_COUNT["Brasil"] = COUNTRY_COUNT.pop("Brazil")
        COUNTRY_COUNT["Sverige"] = COUNTRY_COUNT.pop("Sweden")
        COUNTRY_COUNT["Nederland"] = COUNTRY_COUNT.pop("TheNetherlands")
        COUNTRY_COUNT["Colombia"] = COUNTRY_COUNT.pop("Columbia")


def print_dict():
    for k, v in COUNTRY_COUNT.items():
        print(k, ': ', v)


if __name__ == "__main__":
    make_country_code_dict()
    start()
    fix_dictionary()
    print_dict()
    time.sleep(3)
    make_js_file()

