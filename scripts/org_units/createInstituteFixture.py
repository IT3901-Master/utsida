import json

institutes = []

def parse_api():
	# stores the api as a json object
	with open("org_units.json") as data_file:
		data = json.load(data_file)

	# defines the path to where the faculties start in the api
	path_to_faculties = data["orgUnit"][0]["subUnit"][0]["subUnit"]

	# iterating over all faculties
	for i in range(9, 16):
		num_institutes = len(path_to_faculties[i]["subUnit"])
		for j in range(0, num_institutes):
			if path_to_faculties[i]["subUnit"][j]["category"] == "Institutt":
				institute = {}
				fields = {}
				fields["name"] = path_to_faculties[i]["subUnit"][j]["name"]
				fields["faculty"] = path_to_faculties[i]["acronym"]
				institute["pk"] = path_to_faculties[i]["subUnit"][j]["acronym"]
				institute["model"] = "utsida.institute"

				institute["fields"] = fields

				institutes.append(institute) 


def to_json():
	json_data = json.dumps(institutes)

	target = open("../../utsida/fixtures/institutes.json", "w")

	target.write(json_data)

	target.close()


if __name__ == '__main__':
	parse_api()
	to_json()







