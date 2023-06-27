import pandas as pd

# Load the data
pollutants = pd.read_csv('pollutants.csv', sep=';')
health = pd.read_csv('../EuroStat - Health Data/health.csv', sep=';')

# Check for which of the city_code values in the health.csv file there exist values under NUTS2 value
common_city_codes = set(pollutants['NUTS2']).intersection(set(health['city_code']))

output_file = open('output.txt', 'w')

# loop through the common city codes
for city_code in common_city_codes:
    # get all the pollutant data for that city code
    city_code_pollutants = pollutants[pollutants['NUTS2'] == city_code]
    
    # find all pollutants
    pollutants_list = list(city_code_pollutants['Air Pollutant'].unique())

    output_file.write(city_code + '\n')

    for pollutant in pollutants_list:
        output_file.write('\t' + pollutant + ': ')
        # find all the years that fit both the code and pollutant
        years = list(city_code_pollutants[city_code_pollutants['Air Pollutant'] == pollutant]['Year'].unique())
        for year in years:
            output_file.write(str(year) + ', ')
        output_file.write('\n')

    output_file.write('\n')

output_file.close()