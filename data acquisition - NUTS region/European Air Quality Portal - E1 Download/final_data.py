import os
import pandas as pd

pollutants = ["5", "10", "38", "8", "7", "1"]

for pollutant in pollutants:
    csv_files = []
    for file in os.listdir("./Downloaded files"):
        print(file)
        if(file.endswith(f"-{pollutant}.csv")):
            csv_files.append(file)

    print(csv_files)

    df_list = []
    first_file = True
    headers = None

    for file in csv_files:
        print(file)
        country, city = file.split("-")[0:2]
        df = pd.read_csv("Downloaded files/" + file, encoding='utf-8', sep=',')
        if first_file:
            headers = df.columns
            first_file = False
        elif not df.columns.equals(headers):
            print(f"Headers in {file} do not match the first file's headers.")
            continue

        df["Country"] = country
        df["City"] = city

        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv(f"combined-{pollutant}.csv", index=False, encoding='utf-8', sep=';')
