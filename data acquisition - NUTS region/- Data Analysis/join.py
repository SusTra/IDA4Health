import pandas as pd


#! INPUT file
def create_input_file():
    # load data
    df = pd.read_csv("../European Air Quality Portal - E1 Download/pollutants.csv", encoding="utf-8", sep=";")

    # Aggregate the average across multiple years for each location and type
    df_avg = df.groupby(['city', 'Pollutant'])['Average Concentration'].mean().reset_index()

    # Pivot the data so each type is in its own column
    df_pivot = df_avg.pivot(index='city', columns='Pollutant', values='Average Concentration').reset_index()

    # rename the city column to NUTS Region
    df_pivot = df_pivot.rename(columns={"city": "NUTS Region"})

    # Save the output
    df_pivot.to_csv('input.csv', index=False, encoding="utf-8", sep=";")

#! CONTROL file
def create_control_file():
    # load data
    df = pd.read_csv("../EuroStat - GDP/GDP.csv", encoding="utf-8", sep=";")

    # Aggregate the average across multiple years for each location and type
    df_avg = df.groupby(['city_name', 'unit'])['value'].mean().reset_index()

    # Pivot the data so each type is in its own column
    df_pivot = df_avg.pivot(index='city_name', columns='unit', values='value').reset_index()

    # rename the city column to NUTS Region
    df_pivot = df_pivot.rename(columns={"city_name": "NUTS Region"})

    # Save the output
    df_pivot.to_csv('control_1.csv', index=False, encoding="utf-8", sep=";")

#! OUTPUT file
def create_output_file():
    # load data
    df = pd.read_csv("../EuroStat - Health Data/health.csv", encoding="utf-8", sep=";")

    # Aggregate the average across multiple years for each location and type
    df_avg = df[df["sex"] == "Total"].groupby(['city_name', 'name', "sex"])['value'].mean().reset_index()

    # Pivot the data so each type is in its own column
    df_pivot = df_avg.pivot(index='city_name', columns='name', values='value').reset_index()

    # rename the city column to NUTS Region
    df_pivot = df_pivot.rename(columns={"city_name": "NUTS Region"})

    # Save the output
    df_pivot.to_csv('output.csv', index=False, encoding="utf-8", sep=";")

create_input_file()
create_control_file()
create_output_file()