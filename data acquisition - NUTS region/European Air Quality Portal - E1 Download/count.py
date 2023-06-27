# open the file called pollutants.csv

import pandas as pd

df = pd.read_csv("pollutants.csv", encoding='utf-8', sep=';')

# find all the unique pollutants
pollutants = df["Pollutant"].unique()
for pollutant in pollutants:
    # find all the NUTS reagions with this pollutant
    rows = df.loc[df['Pollutant'] == pollutant]
    # print the name of the pollutant and the number of NUTS regions
    print(f"{pollutant}: {len(rows)}")
    # find the NUTS region with the highest average value
    max_row = rows.loc[rows['Average Concentration'] == rows['Average Concentration'].max()]
    # print the name of the NUTS region with the highest average value
    print(f"Max: {max_row.iloc[0]['NUTS']} with value {max_row.iloc[0]['Average Concentration']}")
    # find the NUTS region with the lowest average value
    min_row = rows.loc[rows['Average Concentration'] == rows['Average Concentration'].min()]
    # print the name of the NUTS region with the lowest average value
    print(f"Min: {min_row.iloc[0]['NUTS']} with value {min_row.iloc[0]['Average Concentration']}")