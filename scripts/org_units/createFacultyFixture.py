import json

faculties = []


def parse_api():
	# stores the api as a json object
	with open("org_units.json") as data_file:
		data = json.load(data_file)

	# defines the path to where the faculties start in the api
	path_to_faculties = data["orgUnit"][0]["subUnit"][0]["subUnit"]

	# iterating over all faculties
	for i in range(9, 16):
		faculty = {}
		faculty["fields"] = {}
		faculty["fields"]["name"] = path_to_faculties[i]["name"]
		faculty["pk"] = path_to_faculties[i]["acronym"]
		faculty["model"] = "utsida.faculty"
		
		faculties.append(faculty)

def to_json():
	json_data = json.dumps(faculties)

	target = open("../../utsida/fixtures/faculties.json", "w")

	target.write(json_data)

	target.close()


if __name__ == '__main__':
	parse_api()
	to_json()








