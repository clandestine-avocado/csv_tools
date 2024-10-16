import csv
import os
import datetime
import re

def analyze_csv(file_path):
    log = []
    issues = {}
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            content = csvfile.read()
            dialect = csv.Sniffer().sniff(content)
            has_header = csv.Sniffer().has_header(content)
            
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            
            headers = next(reader) if has_header else None
            rows = list(reader)
            
            # Summary data
            log.append("CSV File Summary:")
            log.append(f"File: {file_path}")
            log.append(f"Total number of records: {len(rows) + (1 if has_header else 0)}")
            log.append(f"Has header: {has_header}")
            if headers:
                log.append(f"Field names: {', '.join(headers)}")
                log.append(f"Number of fields: {len(headers)}")
            log.append(f"Delimiter: '{dialect.delimiter}'")
            log.append(f"Quote character: '{dialect.quotechar}'")
            log.append(f"Escape character: '{dialect.escapechar if dialect.escapechar else 'None'}'")
            
            # Analyze potential issues
            log.append("\nPotential Issues:")
            
            # Check for inconsistent number of fields
            expected_field_count = len(headers) if headers else len(rows[0])
            issues['inconsistent_fields'] = [(i, len(row)) for i, row in enumerate(rows, start=2) if len(row) != expected_field_count]
            
            if issues['inconsistent_fields']:
                log.append("1. Inconsistent number of fields detected:")
                for row_num, field_count in issues['inconsistent_fields']:
                    log.append(f"   Row {row_num}: Expected {expected_field_count} fields, found {field_count}")
                
                # Analyze possible causes
                log.append("   Possible causes:")
                
                # Check for unescaped delimiters in quoted fields
                unescaped_delimiters = [i for i, row in enumerate(rows, start=2) 
                                        if any(field.count('"') % 2 != 0 and dialect.delimiter in field for field in row)]
                if unescaped_delimiters:
                    log.append(f"   - Unescaped delimiters in quoted fields in rows: {unescaped_delimiters}")
                
                # Check for mismatched quotes
                mismatched_quotes = [i for i, row in enumerate(rows, start=2) 
                                     if any(field.count('"') % 2 != 0 for field in row)]
                if mismatched_quotes:
                    log.append(f"   - Mismatched quotes in rows: {mismatched_quotes}")
                
                # Check for line breaks within fields
                line_breaks = [i for i, row in enumerate(rows, start=2) 
                               if any('\n' in field or '\r' in field for field in row)]
                if line_breaks:
                    log.append(f"   - Line breaks within fields in rows: {line_breaks}")
                
                # Check for empty fields at the end of rows
                empty_end_fields = [i for i, row in enumerate(rows, start=2) 
                                    if len(row) > expected_field_count and all(field.strip() == '' for field in row[expected_field_count:])]
                if empty_end_fields:
                    log.append(f"   - Empty fields at the end of rows: {empty_end_fields}")
                
                log.append("   - For rows with fewer fields than expected, check for missing data or incorrect delimiters")
                log.append("   - Manual inspection may be required for complex cases")
            
            # Check for unnecessary quoting
            issues['unnecessary_quoting'] = [i for i, row in enumerate(rows, start=2) 
                                             if any(field.startswith('"') and field.endswith('"') and dialect.delimiter not in field 
                                                    for field in row)]
            if issues['unnecessary_quoting']:
                log.append(f"2. Unnecessary quoting detected in rows: {issues['unnecessary_quoting']}")
            
            # Check for escaped characters
            if dialect.escapechar:
                issues['escaped_chars'] = [i for i, row in enumerate(rows, start=2) 
                                           if any(dialect.escapechar in field for field in row)]
                if issues['escaped_chars']:
                    log.append(f"3. Escaped characters found in rows: {issues['escaped_chars']}")
            
            # Check for line returns within fields (if not already reported)
            if not line_breaks:
                issues['line_returns'] = [i for i, row in enumerate(rows, start=2) 
                                          if any('\n' in field or '\r' in field for field in row)]
                if issues['line_returns']:
                    log.append(f"4. Line returns found within fields in rows: {issues['line_returns']}")
            
            # Check for leading/trailing whitespace
            issues['whitespace'] = [i for i, row in enumerate(rows, start=2) 
                                    if any(field.strip() != field for field in row)]
            if issues['whitespace']:
                log.append(f"5. Leading or trailing whitespace found in rows: {issues['whitespace']}")
            
            # Check for potential data type inconsistencies
            if headers:
                log.append("6. Data type analysis:")
                for i, field_name in enumerate(headers):
                    numeric_rows = [j for j, row in enumerate(rows, start=2) if len(row) > i and row[i].strip().isdigit()]
                    float_rows = [j for j, row in enumerate(rows, start=2) if len(row) > i and row[i].strip().replace('.', '').isdigit()]
                    date_rows = [j for j, row in enumerate(rows, start=2) if len(row) > i and re.match(r'\d{4}-\d{2}-\d{2}', row[i].strip())]
                    
                    if len(numeric_rows) == len(rows):
                        log.append(f"   - Field '{field_name}' contains only numeric values")
                    elif len(float_rows) == len(rows):
                        log.append(f"   - Field '{field_name}' may contain floating-point values")
                    elif len(date_rows) == len(rows):
                        log.append(f"   - Field '{field_name}' may contain date values")
                    else:
                        mixed_type_rows = set(range(2, len(rows) + 2)) - set(numeric_rows) - set(float_rows) - set(date_rows)
                        if mixed_type_rows:
                            log.append(f"   - Field '{field_name}' has mixed data types in rows: {list(mixed_type_rows)}")

    except Exception as e:
        log.append(f"Error analyzing file: {str(e)}")
    
    return log

def write_log(log_entries):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"csv_analysis_{timestamp}.log"
    
    with open(log_file, 'w', encoding='utf-8') as logfile:
        logfile.write("\n".join(log_entries))
    
    print(f"Analysis complete. Log file created: {log_file}")

if __name__ == "__main__":
    csv_file = input("Enter the path to the CSV file: ")
    if os.path.exists(csv_file):
        log_entries = analyze_csv(csv_file)
        write_log(log_entries)
    else:
        print("File not found. Please check the file path and try again.")