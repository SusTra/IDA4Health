import requests
import json
data = ""
with open('temp_cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# filter cities such that if the second element of the elmenet is empty, then remove it
cities = []
for i in range(len(data)):
    if data[i][1] != "":
        cities.append(data[i])

print(cities)

final_data = []

for country, city in cities:
    api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}&country='.format(city, country)
    response = requests.get(api_url + city, headers={'X-Api-Key': 'brVrODPEhjcRu7v7hrqmFQ==T3gnEEaTQgnkhu19'})
    if response.status_code == requests.codes.ok:
        final_data.append(response.json())
    else:
        print("Error:", response.status_code, response.text)

# dump final data to json file
with open('final_data.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)