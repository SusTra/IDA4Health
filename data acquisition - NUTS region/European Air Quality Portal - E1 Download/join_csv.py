# loop through all folders without recurssion in the folder downloaded files

import os
import pandas as pd


def join_csv(folder):
    # check if the folder is empty
    if(len(os.listdir(folder)) == 0):
        # delete the dfolder
        os.rmdir(folder)
        return None

    # join all the csv files in the folder into a csv called 
    # find all the csv files in the folder

    csv_files = []
    for file in os.listdir(folder):
        if(file.endswith(".csv")):
            csv_files.append(file)
    
    df_list = []
    first_file = True
    headers = None

    for file in csv_files:
        df = pd.read_csv(folder + "/" + file, encoding='utf-8', sep=',')
        if first_file:
            headers = df.columns
            first_file = False
        elif not df.columns.equals(headers):
            print(f"Headers in {file} do not match the first file's headers.")
            continue

        df_list.append(df)

    try:
        combined_df = pd.concat(df_list, ignore_index=True)
    except:
        return None
    return combined_df

for folder in os.listdir("Downloaded files"):
    if(os.path.isdir(f"Downloaded files/{folder}")):
        for subfolder in os.listdir(f"Downloaded files/{folder}"):
            if(os.path.isdir(f"Downloaded files/{folder}/{subfolder}")):
                data = join_csv(f"Downloaded files/{folder}/{subfolder}")  
                if data is not None:
                    data.to_csv(f"Downloaded files/{folder}-{subfolder}.csv", index=False)