import pandas as pd
import re

def check_extra_quotes(file_path, delimiter='|', sample_size=10000):
    # ... [previous code remains the same] ...

def fix_extra_quotes(file_path, output_path, delimiter='|'):
    # Read the CSV file
    df = pd.read_csv(file_path, delimiter=delimiter, quoting=3)  # quoting=3 means no quoting
    
    # Function to remove extra quotes
    def remove_quotes(value):
        if isinstance(value, str):
            return re.sub(r'^"(.*)"$', r'\1', value.strip())
        return value
    
    # Apply the function to all string columns
    for column in df.select_dtypes(include=['object']):
        df[column] = df[column].apply(remove_quotes)
    
    # Write the cleaned data to a new CSV file
    df.to_csv(output_path, index=False, quoting=1)  # quoting=1 means quote as needed

# Usage
check_extra_quotes('your_file.csv', delimiter='|')
fix_extra_quotes('your_file.csv', 'cleaned_file.csv', delimiter='|')