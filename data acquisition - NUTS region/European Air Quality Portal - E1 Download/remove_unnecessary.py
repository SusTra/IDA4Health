# open csv file called ../EuroStat (Meta) - Cities/city_codes.csv
# open csv fill called pollutants_temp.csv

import pandas as pd

cities_df = pd.read_csv("../EuroStat (Meta) - Cities/city_codes.csv", encoding='utf-8', sep=';')
pollutants_df = pd.read_csv("pollutants_temp.csv", encoding='utf-8', sep=';')

# join together the two dataframes by code in first and NUTS in second
joined_df = pd.merge(cities_df, pollutants_df, left_on='code', right_on='NUTS', how='inner')

# save the joined dataframe to a csv file
joined_df.to_csv("pollutants.csv", index=False, encoding='utf-8', sep=';')