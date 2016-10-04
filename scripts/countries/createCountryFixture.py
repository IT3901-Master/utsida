import json

countries = {}
file_country = []
file_continent = []

europe_countries = []
na_countries = []
sa_countries = []
asia_countries = []
oceania_countries = []
africa_countries = []


def fill_country_lists():
    target_eu = open("data/europe.txt", "r")
    for line in target_eu:
        europe_countries.append(line.rstrip('\n'))
        countries["europe"] = europe_countries
    target_eu.close()

    target_na = open("data/na.txt", "r")
    for line in target_na:
        na_countries.append(line.rstrip('\n'))
        countries["na"] = na_countries
    target_eu.close()

    target_sa = open("data/sa.txt", "r")
    for line in target_sa:
        sa_countries.append(line.rstrip('\n'))
        countries["sa"] = sa_countries
    target_sa.close()

    target_asia = open("data/asia.txt", "r")
    for line in target_asia:
        asia_countries.append(line.rstrip('\n'))
        countries["asia"] = asia_countries
    target_asia.close()

    target_africa = open("data/africa.txt", "r")
    for line in target_africa:
        africa_countries.append(line.rstrip('\n'))
        countries["africa"] = africa_countries
    target_africa.close()

    target_oceania = open("data/oceania.txt", "r")
    for line in target_oceania:
        oceania_countries.append(line.rstrip('\n'))
        countries["oceania"] = oceania_countries
    target_oceania.close()


def make_file():
    counter = 1
    counter_continent = 1
    for key, value in countries.items():
        new_continent = {}
        new_continent["pk"] = key
        new_continent["model"] = "utsida.continent"
        new_continent["fields"] = {}
        #new_continent["fields"]["name"] = key
        counter_continent += 1
        file_continent.append(new_continent)

        for country in value:
            new_country = {}
            new_country["pk"] = country
            new_country["model"] = "utsida.country"
            new_country["fields"] = {}
            new_country["fields"]["continent"] = key
            #new_country["fields"]["name"] = country

            file_country.append(new_country)
            counter += 1


def to_json():
    json_data_country = json.dumps(file_country)
    json_data_continent = json.dumps(file_continent)

    target_country = open("../../utsida/fixtures/countries.json", "w")

    target_continent = open("../../utsida/fixtures/continents.json", "w")

    target_country.write(json_data_country)
    target_continent.write(json_data_continent)

    target_country.close()
    target_continent.close()


if __name__ == '__main__':
    fill_country_lists()
    make_file()
    to_json()
