import pandas as pd
import itertools

# Load data
df = pd.read_csv('pollutants.csv', sep=';')

# Find unique values
unique_years = df['Year'].unique()
unique_NUTS2 = df['NUTS2'].unique()
unique_air_pollutant = df['Air Pollutant'].unique()

# Generate all possible combinations
all_combinations = list(itertools.product(unique_years, unique_NUTS2, unique_air_pollutant))

# Convert original data to tuple for comparison
original_combinations = list(df[['Year', 'NUTS2', 'Air Pollutant']].itertuples(index=False, name=None))

# Open files to write results
with open('is_present.txt', 'w') as present_file, open('are_not.txt', 'w') as not_present_file:
    for combination in all_combinations:
        if combination in original_combinations:
            present_file.write(f'{combination}\n')
        else:
            not_present_file.write(f'{combination}\n')
