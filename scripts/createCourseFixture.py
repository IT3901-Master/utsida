
from urllib.request import urlopen
import simplejson
import json

response = urlopen("http://www.ime.ntnu.no/api/course/en/-")
data = simplejson.load(response)
output = []

for x in range(0,len(data["course"])):
    information = data["course"][x]
    newDict = {}
    newDict["model"] = "utsida.homecourse"
    newDict["pk"] = x

    fields = {}
    fields["code"] = information["code"]
    fields["name"] = information["name"]
    fields["description_url"] = ""
    newDict["fields"] = fields


    output.append(newDict)
    print(information["code"])
    print(information["name"])

print(output)

with open('homeCourses.json', 'w') as outfile:
  json.dump(output, outfile)


