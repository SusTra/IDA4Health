import pandas as pd

input_file = "data.csv"
output_file = "../crime.csv"
cities_file = "../../EuroStat (Meta) - Cities/city_codes.csv"

iccs_dict = {
    "TOTAL": "Total",
    "ICCS01":	"Acts leading to death or intending to cause death",
    "ICCS0101_0102":	"Intentional homicide and attempted intentional homicide",
    "ICCS0101":	"Intentional homicide",
    "ICCS0102":	"Attempted intentional homicide",
    "ICCS02-04": "Acts causing harm or intending to cause harm to the person, injurious acts of a sexual nature and acts against property involving violence or threat against a person",
    "ICCS02":	"Acts causing harm or intending to cause harm to the person",
    "ICCS0201":	"Assaults and threats",
    "ICCS02011":	"Assault",
    "ICCS020111":	"Serious assault",
    "ICCS0202":	"Acts against liberty",
    "ICCS02022":	"Deprivation of liberty",
    "ICCS020221":	"Kidnapping",
    "ICCS0204":	"Trafficking in persons",
    "ICCS02041":	"Trafficking in persons for sexual exploitation",
    "ICCS02042":	"Trafficking in persons for forced labour or services",
    "ICCS02043_02044":	"Trafficking in persons for organ removal and other purposes",
    "ICCS03":	"Injurious acts of a sexual nature",
    "ICCS0301":	"Sexual violence",
    "ICCS03011":	"Rape",
    "ICCS03012":	"Sexual assault",
    "ICCS03019":	"Other acts of sexual violence",
    "ICCS0302":	"Sexual exploitation",
    "ICCS03022":	"Sexual exploitation of children",
    "ICCS04":	"Acts against property involving violence or threat against a person",
    "ICCS0401":	"Robbery",
    "ICCS05":	"Acts against property only",
    "ICCS0501":	"Burglary",
    "ICCS05012":	"Burglary of private residential premises",
    "ICCS0502":	"Theft",
    "ICCS05021":	"Theft of a motorized vehicle or parts thereof",
    "ICCS050211":	"Theft of a motorized land vehicle",
    "ICCS06":	"Acts involving controlled drugs or other psychoactive substances",
    "ICCS0601":	"Unlawful acts involving controlled drugs or precursors",
    "ICCS07":	"Acts involving fraud, deception or corruption",
    "ICCS08":	"Acts against public order, authority and provisions of the State",
    "ICCS09":	"Acts against public safety and state security",
    "ICCS10":	"Acts against the natural environment",
    "ICCS11":	"Other criminal acts not elsewhere classified",
}

# Read data
input_data = pd.read_csv(input_file, sep=",", header=0,
                         index_col=0, encoding="utf-8")
cities_data = pd.read_csv(cities_file, sep=";", header=0,
                          index_col=0, encoding="utf-8")

# the cities data contains the city code and city name
# the input data contains the city code and the area
# we want to merge the two dataframes to get the city name and the area

# merge the two dataframes.  Mind that the names of the columns are not the same
merged_data = pd.merge(input_data, cities_data, left_on="geo", right_on="code")

# keep only the city name and the area
merged_data = merged_data[["city", "geo", "OBS_VALUE", "TIME_PERIOD", "iccs"]]

# rename the columns
merged_data.columns = ["city_name", "city_code", "value", "measurement_date", "name"]

# for each name, replace the code with the name of the crime
merged_data["name"] = merged_data["name"].map(iccs_dict)

# add a column called unit, one called measurement date, and hierarchy
merged_data["unit"] = "1"


# dump the data to a csv file without indexing it
merged_data.to_csv(output_file, sep=";", encoding="utf-8", index=False)
