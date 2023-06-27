import pandas as pd

input_files = ["data1.csv", "data2.csv", "data3.csv", "data4.csv"]
output_file= "../education.csv"
cities_file= "../../EuroStat (Meta) - Cities/city_codes.csv"

aes_dict= {
"POP": "Population",
"ACT": "Persons in the labour force (former name: active persons)",
"EMP": "Employed persons",
"UNE": "Unemployed persons",
"INAC": "Persons outside the labour force (former name: inactive persons)",
"UNK": "Unknown"
}

ed_dict= {
"TOTAL": "All ISCED 1997 levels",
"ED1": "Primary education or first stage of basic education (level 1)",
"ED2": "Lower secondary or second stage of basic education (level 2)",
"ED3": "Upper secondary education (level 3)",
"ED4": "Post-secondary non-tertiary education (level 4)",
"ED5": "First stage of tertiary education not leading directly to an advanced research qualification (level 5)",
"ED6": "Second stage of tertiary education leading to an advanced research qualification (level 6)",
"NED": "No education",
"NAP": "Not applicable",
"UNK": "Unknown"
}

sex_dict = {
    "T": "Total",
    "M": "Males",
    "F": "Females"
}

age_dict = {
"TOTAL" : "Total",
"Y_LT5" : "Less than 5 years",
"Y5-9" : "From 5 to 9 years",
"Y10-14" : "From 10 to 14 years",
"Y_LT15" : "Less than 15 years",
"Y15-19" : "From 15 to 19 years",
"Y15-29" : "From 15 to 29 years",
"Y20-24" : "From 20 to 24 years",
"Y25-29" : "From 25 to 29 years",
"Y30-34" : "From 30 to 34 years",
"Y30-49" : "From 30 to 49 years",
"Y35-39" : "From 35 to 39 years",
"Y40-44" : "From 40 to 44 years",
"Y45-49" : "From 45 to 49 years",
"Y50-54" : "From 50 to 54 years",
"Y50-64" : "From 50 to 64 years",
"Y55-59" : "From 55 to 59 years",
"Y60-64" : "From 60 to 64 years",
"Y65-69" : "From 65 to 69 years",
"Y65-84" : "From 65 to 84 years",
"Y70-74" : "From 70 to 74 years",
"Y75-79" : "From 75 to 79 years",
"Y80-84" : "From 80 to 84 years",
"Y85-89" : "From 85 to 89 years",
"Y_GE85" : "85 years or over",
"Y90-94" : "From 90 to 94 years",
"Y95-99" : "From 95 to 99 years",
"Y_GE100" : "100 years or over",
}

# Read data
input_data= pd.concat([pd.read_csv(input_file, sep=",", header=0,
                       index_col=0, encoding="utf-8") for input_file in input_files])
cities_data= pd.read_csv(cities_file, sep=";", header=0,
                          index_col=0, encoding="utf-8")

# the cities data contains the city code and city name
# the input data contains the city code and the area
# we want to merge the two dataframes to get the city name and the area

# merge the two dataframes.  Mind that the names of the columns are not the same
merged_data= pd.merge(input_data, cities_data, left_on="geo", right_on="code")

# keep only the city name and the area
merged_data= merged_data[["city", "geo", "age", "sex",
                           "wstatus", "isced97", "TIME_PERIOD", "OBS_VALUE"]]

# rename the columns
merged_data.columns= ["city_name", "city_code",
                       "age", "sex", "activity and employment status", "education level", "year", "value"]
# for each name, replace the code with the name of the crime
merged_data["unit"]= "Number"

# replace the codes with the names
merged_data["activity and employment status"]= merged_data["activity and employment status"].replace(aes_dict)
merged_data["education level"]= merged_data["education level"].replace(ed_dict)
merged_data["age"]= merged_data["age"].replace(age_dict)
merged_data["sex"]= merged_data["sex"].replace(sex_dict)

# dump the data to a csv file without indexing it
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)
