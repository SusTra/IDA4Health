import pandas as pd

input_file = "data.csv"
output_file = "../GDP.csv"
cities_file = "../../EuroStat (Meta) - Cities/city_codes.csv"

unit_dict = {
    "MIO_EUR":  "Million euro",
    "EUR_HAB":  "Euro per inhabitant",
    "EUR_HAB_EU27_2020":  "Euro per inhabitant in percentage of the EU27 (from 2020) average",
    "MIO_NAC":  "Million units of national currency",
    "MIO_PPS_EU27_2020":  "Million purchasing power standards (PPS, EU27 from 2020)",
    "PPS_EU27_2020_HAB":  "Purchasing power standard (PPS, EU27 from 2020), per inhabitant",
    "PPS_HAB_EU27_2020":  "Purchasing power standard (PPS, EU27 from 2020), per inhabitant in percentage of the EU27 (from 2020) average",
}

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
merged_data = merged_data[["city", "geo", "OBS_VALUE", "TIME_PERIOD", "unit"]]

# rename the columns
merged_data.columns = ["city_name", "city_code", "value", "measurement_date", "unit"]

# for each name, replace the code with the name of the crime
merged_data["unit"] = merged_data["unit"].map(unit_dict)

# add a column called unit, one called measurement date, and hierarchy
merged_data["name"] = "GDP"


# dump the data to a csv file without indexing it
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)
