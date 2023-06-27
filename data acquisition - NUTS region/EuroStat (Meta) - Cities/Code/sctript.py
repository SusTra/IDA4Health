# read all the data from data.csv file and find all the cities with the common name. For each name, display the codes that go along with  it

import csv 
import pandas as pd

df = pd.read_csv("data.csv", encoding="utf-8", sep=";")

cities = {}

output_file_city_name = "../cities.csv"
output_file_city_code = "../city_codes.csv"

for index, row in df.iterrows():
    if(row["Name"] not in cities):
        cities[row["Name"]] = []
    cities[row["Name"]].append(row["Code"])

file1 = open(output_file_city_name, "w", encoding="utf-8")
file2 = open(output_file_city_code, "w", encoding="utf-8")

file1.write("City\n")
file2.write("Code;City\n")

for city in cities:
    file1.write(city + "\n")
    for code in cities[city]:
        file2.write(code + ";" + city + "\n")