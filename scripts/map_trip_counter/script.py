import json
import codecs

count_data = {}
code_data = []
new_data = []

def fillTripCount():
	file = open('cases.csv', 'r')

	unique_countries = []

	for line in file:
		country = line.split(';')[2]
		if not country in unique_countries:
			unique_countries.append(country)
			count_data[country] = 0
			count_data[country] += 1
		if country in unique_countries:
			count_data[country] += 1


	file.close()

def fillLandCodeData():

	file = codecs.open('377.csv', encoding='latin-1')

	for line in file:
		obj = {}

		code = line.split(';')[0]
		name = line.split(';')[2]

		obj['code'] = code
		obj['name'] = name.strip()

		code_data.append(obj)

	file.close()

	del code_data[0]


def mergeData():

	for name, num in count_data.items():
		new_obj = {}
		for line in code_data:
			if name == line['name']:
				new_obj['code'] = line['code']
				new_obj['trips'] = num

		new_data.append(new_obj)


def makeJavaScript():
	target = open('country_codes.js', 'w')

	target.write("var country_code_data = {")

	counter = 0

	for line in new_data:
		try:
			if counter == len(new_data) - 1:
				target.write("'" + str(line["code"]) + "': " + str(line['trips']))
				target.write('}')
			else:
				target.write("'" + str(line["code"]) + "': " + str(line['trips']) + ',')
				counter += 1
		
		except KeyError:
			counter += 1
			pass



if __name__ == '__main__':
	fillTripCount()
	fillLandCodeData()
	mergeData()
	makeJavaScript()
























'''
for k, v in data.items():
	if counter == len(data.items()) -1:
		target.write("'" + str(k) + "': " + str(v))
		target.write('}')
	else:
		target.write("'" + str(k) + "': " + str(v) + ',')
	counter += 1
'''
