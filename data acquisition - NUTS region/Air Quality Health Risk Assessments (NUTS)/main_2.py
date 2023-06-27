import os
import pandas as pd
import glob

headers_to_keep = [
    "Country Or Territory",
    "NUTS2",
    "NUTS3",
    "Year",
    "Air Pollutant",
    "Health Risk Scenario",
    "Population",
    "Populated Area [km2]",
    "Air Pollution Average [ug/m3]",
    "Air Pollution Population Weighted Average [ug/m3]"
]

def join_csv_files(directory='.'):
    csv_files = glob.glob(os.path.join(directory, '**/*.csv'), recursive=True)

    if not csv_files:
        print("No CSV files found in the provided directory.")
        return

    df_list = []
    first_file = True
    headers = None

    for file in csv_files:
        df = pd.read_csv(file, encoding='utf-8', sep=',')
        if first_file:
            headers = df.columns
            first_file = False
        elif not df.columns.equals(headers):
            print(f"Headers in {file} do not match the first file's headers.")
            continue

        df = df[headers_to_keep]

        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df


# Run the function and store the resulting dataframe
result = join_csv_files()

# If you want to write the result to a new CSV file, uncomment the line below.
result.to_csv('combined.csv', index=False, encoding='utf-8', sep=';')


