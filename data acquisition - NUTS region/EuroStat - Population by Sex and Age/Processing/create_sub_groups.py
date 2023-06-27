import pandas as pd

#ignore pandas warnings
pd.options.mode.chained_assignment = None  # default='warn'
# disable pandas FutureWarnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

input_file = "data.csv"
output_file = "../demographic_sub_groups.csv"
cities_file = "../../EuroStat (Meta) - Cities/city_codes.csv"

# read the data
input_data = pd.read_csv(input_file, sep=",", header=0,
                            index_col=0, encoding="utf-8")
cities_data = pd.read_csv(cities_file, sep=";", header=0,
                          index_col=0, encoding="utf-8")
merged_data = pd.merge(input_data, cities_data, left_on="geo", right_on="code")
merged_data = merged_data[["city", "geo",
                           "age", "sex", "TIME_PERIOD", "OBS_VALUE"]]
merged_data.columns = ["city_name", "city_code",
                       "age", "sex", "measurement_date", "value"]
merged_data["unit"] = "Number"
sex_dict = {
    "T": "Total",
    "M": "Males",
    "F": "Females"
}
merged_data["sex"] = merged_data["sex"].map(sex_dict)

age_groups = [
    ("Less than 5 years old", 0, 4),
    ("5 to 9 years old", 5, 9),
    ("10 to 14 years old", 10, 14),
    ("15 to 19 years old", 15, 19),
    ("20 to 24 years old", 20, 24),
    ("25 to 29 years old", 25, 29),
    ("30 to 34 years old", 30, 34),
    ("35 to 39 years old", 35, 39),
    ("40 to 44 years old", 40, 44),
    ("45 to 49 years old", 45, 49),
    ("50 to 54 years old", 50, 54),
    ("55 to 59 years old", 55, 59),
    ("60 to 64 years old", 60, 64),
    ("65 to 69 years old", 65, 69),
    ("70 to 74 years old", 70, 74),
    ("75 to 79 years old", 75, 79),
    ("80 to 84 years old", 80, 84),
    ("85 to 89 years old", 85, 89),
    ("90 to 94 years old", 90, 94),
    ("95 to 99 years old", 95, 99),
    ("100 years old or more", 100, 999),
    ("Less than 65 years old", 0, 64),
    ("65 years old or more" , 65, 999),
]

def get_age_code(age):
    if(age >= 1 and age <= 99):
        return "Y" + str(age)
    if(age > 99):
        return "Y_OPEN"
    if(age == 0):
        return "Y_LT1"

for (age_group_name, age_group_lower, age_group_upper) in age_groups:
    print("Creating sub-group: " + age_group_name)
    aggregate = []
    for age in range(age_group_lower, age_group_upper + 1):
        age_code = get_age_code(age)
        aggregate.append(age_code)

    # create a new dataframe with the sub-group
    sub_group_data = merged_data[merged_data["age"].isin(aggregate)]

    # print all column bnames
    print(sub_group_data.columns)

    # sum by city name, year and sex
    for city_code in sub_group_data["city_code"].unique():
        for year in sub_group_data["measurement_date"].unique():
            for sex in sub_group_data["sex"].unique():
                sub_group_value = sub_group_data[(sub_group_data["city_code"] == city_code) &
                                                    (sub_group_data["measurement_date"] == year) &
                                                    (sub_group_data["sex"] == sex)]["value"].sum()
                merged_data = merged_data.append({
                    "city_name": cities_data.loc[city_code]["city"],
                    "city_code": city_code,
                    "age": age_group_name,
                    "sex": sex,
                    "measurement_date": year,
                    "value": sub_group_value,
                    "unit": "Number"
                }, ignore_index=True)


# remove all rows that have the age something that is not in the age_groups list
merged_data = merged_data[merged_data["age"].isin([age_group_name for (age_group_name, age_group_lower, age_group_upper) in age_groups])]

# dump to output
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)