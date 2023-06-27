import pandas as pd

input_file = "data.csv"
output_file = "../demographic.csv"
cities_file = "../../EuroStat (Meta) - Cities/city_codes.csv"

sex_dict = {
    "T": "Total",
    "M": "Males",
    "F": "Females"
}

cities_data = pd.read_csv(cities_file, sep=";", header=0,
                          index_col=0, encoding="utf-8")

input_data = pd.read_csv(input_file, sep=",", header=0,
                         index_col=0, encoding="utf-8")

# the cities data contains the city code and city name
# the input data contains the city code and the area
# we want to merge the two dataframes to get the city name and the area

# merge the two dataframes.  Mind that the names of the columns are not the same
merged_data = pd.merge(input_data, cities_data, left_on="geo", right_on="code")

# remove dupicated names

# keep only the city name and the area
merged_data = merged_data[["city", "geo",
                           "age", "sex", "TIME_PERIOD", "OBS_VALUE"]]

# rename the columns
merged_data.columns = ["city_name", "city_code",
                       "age", "sex", "measurement_date", "value"]

# add a column called unit, one called measurement date, and hierarchy
merged_data["unit"] = "Number"

# replace the codes with the names
merged_data["sex"] = merged_data["sex"].map(sex_dict)

def get_age_name(age_code):
    if(age_code[0] == "Y"):
        try:
            age_number = int(age_code[1:])
            if(age_number > 1):
                return str(age_number) + " years old"
            else:
                return str(age_number) + " year old"
        except:
            if(age_code == "Y_OPEN"):
                return "Open"
            else:
                return "Less than 1 year old"
    else:
        if(age_code == "TOTAL"):
            return "Total"
        else:
            return "Unknown"

# replace the age codes with the names for ages
merged_data["age"] = merged_data["age"].map(get_age_name)

# dump the data to a csv file without indexing it
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)
