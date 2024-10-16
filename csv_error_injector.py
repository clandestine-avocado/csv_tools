import csv
import random

def inject_errors(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        
        for row in reader:
            # Randomly add leading/trailing whitespace
            row = [f" {field} " if random.random() < 0.1 else field for field in row]
            
            # Randomly add line returns within fields
            row = [f"{field}\n" if random.random() < 0.05 else field for field in row]
            
            # Randomly escape some characters
            row = [f"\\{field}" if random.random() < 0.02 else field for field in row]
            
            writer.writerow(row)

    print(f"Modified CSV saved as {output_file}")

# Usage
inject_errors('test_csv_with_errors.csv', 'test_csv_with_errors_modified.csv')