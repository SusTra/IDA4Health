import mysql.connector
import csv

# Configure the MySQL connection
config = {
    'user': 'guhuuoi5k6hh7ixag1wd',
    'password': 'pscale_pw_EK2VvY9HPcNiEiXnsjIAtvonuRrKZgaogQ8wgnZRtxQ',
    'host': 'aws.connect.psdb.cloud',
    'database': 'ida4health',
}

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(**config)
    print('Connected to MySQL database')

    # export data from bulk_insert.csv to the database
    with open('bulk_insert.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        # skip the header row
        next(reader)

        rows = []
        for row in reader:
            rows.append(row)

            # Insert rows in batches of 1000
            if len(rows) == 1000:
                cursor = connection.cursor()
                cursor.executemany(
                    'INSERT INTO location (id, name, description) VALUES (%s, %s, %s)', rows)
                connection.commit()
                cursor.close()
                rows = []

        # Insert any remaining rows
        if rows:
            cursor = connection.cursor()
            cursor.executemany(
                'INSERT INTO location (id, name, description) VALUES (%s, %s, %s)', rows)
            connection.commit()
            cursor.close()

except mysql.connector.Error as error:
    print('Error connecting to MySQL database:', error)

finally:
    # Close the database connection
    if connection.is_connected():
        connection.close()
        print('Disconnected from MySQL database')
