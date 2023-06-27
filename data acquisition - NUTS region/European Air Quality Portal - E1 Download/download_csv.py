# import pandas as pd
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import datetime
from multiprocessing import Pool, freeze_support

input_file = '../EUS Visualization/cities_nuts.csv'

df = pd.read_csv(input_file, sep=';')


def download_csv(url, city_name, country_code, pollutant):
    # check if file exists
    try:
        with open(f"Downloaded files/{country_code}-{city_name}/{pollutant}/{url.split('/')[-1]}", "rb") as f:
            return
    except FileNotFoundError:
        pass

    response = requests.get(url)
    # try creating a folder inside the city foler with the pollutant
    try:
        os.mkdir(f"Downloaded files/{country_code}-{city_name}/{pollutant}")
    except FileExistsError:
        pass

    # download the csv into the pollutant folder
    with open(f"Downloaded files/{country_code}-{city_name}/{pollutant}/{url.split('/')[-1]}", "wb") as f:
        f.write(response.content)



def download_files(country_code, city_name):
    start_year = 2020
    end_year = 2020
    pollutants = ["5", "10", "38", "8", "7", "1"]
    # make a directory called country_code-city_name

    try:
        os.mkdir(f"Downloaded files/{country_code}-{city_name}")
    except FileExistsError:
        pass

    # loop through the pollutants
    for pollutant in pollutants:
        # check if the folder exists
        try:
            os.mkdir(f"Downloaded files/{country_code}-{city_name}/{pollutant}")
        except FileExistsError:
            # if the folder exists, you can skip this pollutant
            continue

        url = f"https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?CountryCode={country_code}&CityName={city_name}&Pollutant={pollutant}&Year_from={start_year}&Year_to={end_year}&Station=&Samplingpoint=&Source=E1a&Output=HTML&UpdateDate=&TimeCoverage=Year"
    
        links = []

        try:
            response = requests.get(url)
            # use bs4 to parse the html and find all the links
            soup = BeautifulSoup(response.text, "html.parser")
            link_elements = soup.find_all("a")
            links = [link_element["href"] for link_element in link_elements]
        except Exception as e:
            print(e)
            pass

        for link in links:
            download_csv(link, city_name, country_code, pollutant)
    
    print(f"Finished downloading files for {country_code}-{city_name}")

if __name__ == "__main__":
    freeze_support()            
    task_args = []

    # looš through each row in the dataframe
    for index, row in df.iterrows():
        # if the NUTS level is not 2, skip
        if row["NUTS level"] != 2:
            continue
        
        task_args.append((row["country"], row["name"]))


    with Pool(5) as p:
        p.starmap(download_files, task_args)