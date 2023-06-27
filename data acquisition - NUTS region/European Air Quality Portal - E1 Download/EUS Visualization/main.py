import json
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd

import re, math
from collections import Counter

from unidecode import unidecode


def strip_accents(text):
    return unidecode(text).lower()

# # open temp.txt and read line by line, saving every line that when split by tabs has two or more rows
# exonyms = []
# with open('temp.txt', 'r', encoding='utf-8') as f:
#     for line in f.readlines():
#         line = line.strip()
#         if line == "":
#             continue
#         line = line.split('\t')
#         if len(line) < 2:
#             continue
#         exonyms.append([line[0].strip(), line[1].strip()])

#         # get rid of the anything that is not a letter or a space in each row
#         for i in range(len(line)):
#             line[i] = ''.join(e for e in line[i] if e.isalpha() or e == ' ')
#         exonyms.append(line[0:2])

# #  remove all that are equal to [name, "language"]
# exonyms = [x for x in exonyms if x[0] != "Name" and x[0] != "English name"]


# # save the exonyms to a json file
# with open('temp_cities.json', 'w', encoding='utf-8') as f:
#     json.dump(exonyms, f, ensure_ascii=False, indent=4)

# load json of temp_cities
exonyms = []
with open('temp_cities.json', 'r', encoding='utf-8') as f:
    exonyms = json.load(f)

# load json data
cities = []
cities_temp = []
with open('../European Air Quality Portal (Meta) - Cities/cities.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)
with open('../European Air Quality Portal (Meta) - Cities/temp_cities.json', 'r', encoding='utf-8') as f:
    cities_temp = json.load(f)
    cities_temp = [x for x in cities_temp if x[1] != '']
print(len(cities), len(cities_temp))

gdf = gpd.read_file('data/NUTS_RG_01M_2021_4326.shp')
print(f"Current CRS: {gdf.crs}")

def find_nuts(lat, long):
    return_data = []
    point = Point(long, lat)
    for i, row in gdf.iterrows():
        if row['geometry'].contains(point):
            return_data.append(row)
    return return_data

data = [
    ["NUTS level", "NUTS value", "country", "name", "latitude", "longitude"],
]


WORD = re.compile(r'\w+')
def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    # each letter that appears should be counted
    # the count of each letter should be divided by the total number of letters

    return Counter(text)

def get_similarity(a, b):
    a = text_to_vector(a.strip().lower())
    b = text_to_vector(b.strip().lower())
    return get_cosine(a, b)

def check_exonym(exonym, name):
    for i in range(len(exonyms)):
        if exonym == exonyms[i][0]:
            if name == exonyms[i][1]:
                return True
    name = strip_accents(name)
    exonym = strip_accents(exonym)


    similarity = get_similarity(exonym, name)
    if(similarity > 0.60):
        return True
    
    for i in range(len(exonyms)):
        if get_similarity(exonym, exonyms[i][0]) > 0.60:
            if get_similarity(name, exonyms[i][1]) > 0.60:
                return True

    print(exonym, name,similarity)
    return False

for i in range(len(cities)):
    city_temp = cities_temp[i]
    for city_geo in cities[i]:
        if city_temp[0] != city_geo['country']:
            continue
        if city_temp[1] != city_geo['name']:
            if (not check_exonym(city_geo['name'], city_temp[1])):
                continue
        rows = find_nuts(city_geo['latitude'], city_geo['longitude'])
        # print(len(rows), city_geo['name'], city_geo['country'],city_temp[0], city_temp[1], city_geo['latitude'], city_geo['longitude'])
        for row in rows:
            data.append([row['LEVL_CODE'], row['NUTS_ID'], city_temp[0], city_temp[1], city_geo['latitude'], city_geo['longitude']])
        break

df = pd.DataFrame(data)
df.to_csv('cities_nuts.csv', index=False, header=False, encoding='utf-8', sep=';')
print(df.head())