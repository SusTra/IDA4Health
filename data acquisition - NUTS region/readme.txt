There are primarily two data sources.
#### 1. We decided which NUTS regions are appropriate for our research.
	1. The data regarding different diseases was available only at the NUTS 2 region so we knew we had to limit ourselves to that resolution.
	2. We arbitrarily chose regions that have a population of les than 5 000 000
	3. This w3as done to reach some level of homogony, as it kept all larger cities but weaved out a lot of the regions that too large
	4. For each of the cities we then saved its NUTS 2 code as well as the name it was referred by

####	2. We then downloaded and processed the data for each of the available regions.
	1. These are all the folders that start with EuroStat
	2. The data was then downloaded in a .csv format, pruned to remove all data that was irrelevant and then outputted as xxxx.csv.
	3. This data was then uploaded to the database

#### 2. Air Quality Health Risk Assessment - WHO
	1. [Source](https://discomap.eea.europa.eu/App/AQViewer/index.html?fqn=Airquality_Dissem.hra.nuts3_sel&EUCountries=Yes&UrbanisationDegree=All%20Areas%20(incl.unclassified)&Year=2020&ScenarioDescription=WHO_2021_AQG_Scen_Base&AirPollutant=PM2.5)
	2. The data here is available by NUTS regions and weighed by population so at first, this data seemed to be optimal. 
	3. First we downloaded all the files using index.js
	4. For each of these, we got a zip file that contained a .csv file
	5. The python files 1 through 4 are then processing the data into a readable format, the fifth file being responsible to calculate the average of NUTS regions and output a file called pollutants.csv
	6. It then became quickly apparent that the coverage of the data was not enough

#### 3. European Air Quality Portal
	1. [Source](https://eeadmz1-cws-wp-air02.azurewebsites.net/index.php/users-corner/download-e1a-from-2013/)
	2. Many of the data sources we found had the problem that we could not find it processed ny NUTS region.
	3. The European Air Quality Portal had data pooled from many different cities across the EU. The data was then acquired for all of these cities.
	4. First the "download_csv.py" file downloaded 6 pollutants for each of the cities that were available
	5. "join_csv.py" then joined all the downloaded files (each file being some measuring device) and joined t hem
	6. "final_data.py" joined all the pollutants for each city into one larger file
	7. "join_by_nuts.py" then combined the cities according to which NUTS 2 region they belonged
		1. EUS Visualization deals with figuring out in which NUTS region the city is
		2. First, it uses an API call to get the coordinates of the city
		3.That is than compared with a cosine similarity with the city as to prevent wrong cities from being mistaken
		3. An Endonym dictionary is also used as many cities have different names
		4. The coordinates are then run through a map of Europe to determine in which NUTS region the city is
	8. "remove_unnecessary.py" then finalizes the data and saves it to pollutants.csv

#### 4. Data Analysis
	1. This is only one of the analysis tools that looks at the correlation between two values and controls for some number of oather values
