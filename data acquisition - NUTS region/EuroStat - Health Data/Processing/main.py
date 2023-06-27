import pandas as pd

input_file = "data.csv"
output_file = "../health.csv"
cities_file = "../../EuroStat (Meta) - Cities/city_codes.csv"

from codes import age_dict
from codes import sex_dict
from codes import icd10_dict

# Read data
input_data = pd.read_csv(input_file, sep=",", header=0,
                         index_col=0, encoding="utf-8")
cities_data = pd.read_csv(cities_file, sep=";", header=0,
                          index_col=0, encoding="utf-8")

# the cities data contains the city code and city name
# the input data contains the city code and the area
# we want to merge the two dataframes to get the city name and the area

# merge the two dataframes.  Mind that the names of the columns are not the same
merged_data = pd.merge(input_data, cities_data, left_on="geo", right_on="code")

# keep only the city name and the area
merged_data = merged_data[["city", "geo", "age", "sex", "TIME_PERIOD", "icd10", "OBS_VALUE"]]

# rename the columns
merged_data.columns = ["city_name", "city_code", "age", "sex", "measurement_date", "name", "value"]

# replace the codes with the actual values
merged_data["age"] = merged_data["age"].map(age_dict)
merged_data["sex"] = merged_data["sex"].map(sex_dict)
merged_data["name"] = merged_data["name"].map(icd10_dict)

# add a column called unit, one called measurement date, and hierarchy
merged_data["unit"] = "Rate"


# dump the data to a csv file without indexing it
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)
