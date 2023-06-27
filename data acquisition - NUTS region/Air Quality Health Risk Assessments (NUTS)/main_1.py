import os
import zipfile

# Get the current working directory
cwd = os.getcwd()

# Find all folders in the current directory
folders = [folder for folder in os.listdir(cwd) if os.path.isdir(folder)]

# Iterate through each folder
for folder in folders:
    folder_path = os.path.join(cwd, folder)

    # Find all files inside the folder
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    # Iterate through each file
    for file in files:
        file_path = os.path.join(folder_path, file)
        file_output_path = file_path.replace('.zip', '')
        data_extract = folder_path + '/DataExtract.csv'

        # Extract the file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)
            print(f'Extracted: {file}')
            os.rename(data_extract, file_output_path)


        print(f'Extracted: {file}')

print('Extraction completed.')
s