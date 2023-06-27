import pandas as pd
import numpy as np

nuts_all_values = {}
nuts_avg_values = {}

output_data = [["NUTS", "City", "Average Concentration", "Pollutant", "Number of Records", "Number of Cities", "UnitOfMeasurement"]]

pollutant_dict = {
    "1": "SO2",
    "5": "PM10",
    "7": "O3",
    "8": "NO2",
    "10": "CO",
    "38": "NO"
}


for pollutant in ["1", "5", "7", "8", "10", "38"]:


    combined_data = pd.read_csv(f"combined-{pollutant}.csv", encoding='utf-8', sep=';')
    # find all the unique cities
    cities = combined_data["City"].unique()

    city_to_nuts = {}
    cities_to_NUTS = pd.read_csv(f"../EUS Visualization/cities_eus.csv", encoding='utf-8', sep=';')
    
    print("Both cities and cities_to_NUTS have been read")

    i = 0
    while i < len(cities):
        city = cities[i]
        i += 1
        # find all the rows with name same and level 2
        rows = cities_to_NUTS.loc[(cities_to_NUTS['name'] == city) & (cities_to_NUTS['NUTS level'] == 2)]
        if len(rows) == 0:
            i-=1
            cities = cities[cities != city]
            print(f"City {city} not found in NUTS")
            continue
        city_to_nuts[city] = rows.iloc[0]["NUTS value"]
    
    print("City to NUTS has been created")
    print(len(cities))

    for city in cities:
        nuts_all_values[city_to_nuts[city]] = []
        nuts_avg_values[city_to_nuts[city]] = -1

    for index, row in combined_data.iterrows():
        try:
            value = float(row["Concentration"])
            nuts_all_values[city_to_nuts[row["City"]]].append(value)
        except KeyError:
            continue
        except ValueError:
            continue
        except Exception as e:
            print(e, row["Concentration"])
            quit()
            continue

    

    for city in cities:
        sum = 0
        count = 0
        for value in nuts_all_values[city_to_nuts[city]]:
            if(np.isnan(value)):
                continue
            sum += float(value)
            count += 1

        avg = sum / count
        nuts_avg_values[city_to_nuts[city]] = avg
        
        output_data.append([city_to_nuts[city], city, avg, pollutant_dict[pollutant], count, len(nuts_all_values[city_to_nuts[city]]), "µg/m3"])
 
    df = pd.DataFrame(output_data)
    df.to_csv(f"pollutants_temp.csv", index=False, encoding='utf-8', sep=';')