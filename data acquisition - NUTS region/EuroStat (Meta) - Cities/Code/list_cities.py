import csv

# Define the paths for the input CSV file and output bulk insert file
input_file = 'data.csv'
output_file = 'cities.csv'

# Open the input CSV file for reading
with open(input_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
        
    # Open the output bulk insert file for writing
    with open(output_file, 'w', newline='\n', encoding='utf-8') as output:
        writer = csv.writer(output, delimiter=';')
        
        # Write the bulk insert header row
        writer.writerow(["name"])
        
        # Process each row from the input CSV file
        id = 0
        previous_name = ""
        for row in reader:
            if(row[1] == previous_name):
                continue
            previous_name = row[1]
            # Format the data fields for bulk insert
            formatted_row = [row[1]]
            id += 1
            
            # Write the formatted row to the output bulk insert file
            writer.writerow(formatted_row)
            
print('Bulk insert file created successfully.')
