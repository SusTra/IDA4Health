import pandas as pd

input_file = "data.csv"
output_file = "../housing.csv"
cities_file = "../../EuroStat (Meta) - Cities/city_codes.csv"

household_dict = {
"TOTAL": "Total",
"FAM1": "Household composed of one-family nucleus",
"MAR": "Household composed of married couple",
"MAR_NCH": "Household composed of married couple without resident children",
"MAR_YCH": "Household composed of married couple with at least one resident child under 25 years",
"MAR_OCH": "Household composed of married couple with youngest resident child 25 years or older",
"REP": "Household composed of couple in registered partnership",
"REP_NCH": "Household composed of couple in registered partnership without resident children",
"REP_YCH": "Household composed of couple in registered partnership with at least one resident child under 25 years",
"REP_OCH": "Household composed of couple in registered partnership with youngest resident child 25 years or older",
"CSU": "Household composed of couple in consensual union",
"CSU_NCH": "Household composed of couple in consensual union without resident children",
"CSU_YCH": "Household composed of couple in consensual union with at least one resident child under 25 years",
"CSU_OCH": "Household composed of couple in consensual union with youngest resident child 25 years or older",
"M1_CH": "Household composed of lone father living with at least one child",
"M1_YCH": "Household composed of lone father with at least one resident child under 25 years",
"M1_OCH": "Household composed of lone father with at least one resident child 25 years or older",
"F1_CH": "Household composed of lone mother living with at least one child",
"F1_YCH": "Household composed of lone mother with at least one resident child under 25 years",
"F1_OCH": "Household composed of lone mother with at least one resident child 25 years or older",
"FAM_GE2": "Household composed of two-or-more-family nucleus",
"NFAM": "Household composed of non-family nucleus",
"P1": "One-person household",
"MULTI": "Multiperson household other than family nucleus"
}

tenure_dict = {
"TOTAL": "Total",
"OWN": "Owner",
"RENT": "Tenant",
"OTH": "Other",
"UNK": "Unknown"
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
merged_data = merged_data[["city", "geo", "hhcomp", "tenure", "TIME_PERIOD", "OBS_VALUE"]]
# rename the columns
merged_data.columns = ["city_name", "city_code", "housing_structure", "tenure", "year", "value"]
# for each name, replace the code with the name of the crime
merged_data["housing_structure"] = merged_data["housing_structure"].map(household_dict)
merged_data["tenure"] = merged_data["tenure"].map(tenure_dict)

# add a column called unit, one called measurement date, and hierarchy
merged_data["unit"] = "Number"


# dump the data to a csv file without indexing it
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)
