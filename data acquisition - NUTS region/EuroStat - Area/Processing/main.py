import pandas as pd

input_file = "data.csv"
output_file = "../areas.csv"
cities_file = "../../EuroStat (Meta) - Cities/city_codes.csv"

# Read data
input_data = pd.read_csv(input_file, sep=",", header=0, index_col=0, encoding="utf-8")
cities_data = pd.read_csv(cities_file, sep=";", header=0, index_col=0, encoding="utf-8")

# the cities data contains the city code and city name
# the input data contains the city code and the area
# we want to merge the two dataframes to get the city name and the area

# merge the two dataframes.  Mind that the names of the columns are not the same
merged_data = pd.merge(input_data, cities_data, left_on="geo", right_on="code")

# keep only the city name and the area
merged_data = merged_data[["city", "geo", "OBS_VALUE"]]

# rename the columns
merged_data.columns = ["city_name", "city_code", "value"]

# add a column called unit, one called measurement date, and hierarchy
merged_data["unit"] = "km2"
merged_data["measurement date"] = "2022"
merged_data["name"] = "Area by EuroStat"


# dump the data to a csv file without indexing it
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)
