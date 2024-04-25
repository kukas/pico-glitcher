import csv

# this script will check if the data in the csv file is correct
# use on wiped chip (wiper.py) where dummy data has been written to
# the flash (writer.py) and the data has been read using exploit.py

csv_file_path = 'data.csv'
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    
    for row in list(csv_reader)[:500]:
        if len(row) >= 2:  # Ensure the row has at least two columns
            first_value = int(row[0])%256  # Convert first column to integer
            second_value = int(row[1])  # Convert second column to integer
            
            if first_value != second_value:
                print(f"Values do not match: {row[0]} != {row[1]}")
        else:
            print("Error: Row does not have enough columns.")
