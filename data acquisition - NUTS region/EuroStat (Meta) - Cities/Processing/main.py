import pandas as pd
from geo_dict import geo_dict

input_file = "data.csv"
output_file = "../city_codes.csv"
output_file2 = "../cities.csv"

# Read data
input_data = pd.read_csv(input_file, sep=",", header=0, index_col=0, encoding="utf-8")


# sort all data by OBS_VALUE and remove any that have a value over 5 000 000
input_data = input_data.sort_values(by="OBS_VALUE")
input_data = input_data[input_data["OBS_VALUE"] < 5000000]

# keep only the OBS value and geo
input_data = input_data[["geo"]]
# rename
input_data = input_data.rename(columns={"geo": "code"})
# remove first column
input_data.index.name = None

# add another colum called city name and get it from the geo_dict
input_data["city"] = input_data["code"].apply(lambda x: geo_dict[x])

# dump
input_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)

# remove the name
input_data = input_data[["city"]]
# remove duplicates
input_data = input_data.drop_duplicates()
# dump
input_data.to_csv(output_file2, sep=";", encoding="utf-8", index=False)