import csv
import json
from constants import UNIVERSAL_ENCODING
def convert_csv_to_json(csv_file, json_file):
    data = []
    
    # Open the CSV file for reading
    with open(csv_file, mode='r', encoding=UNIVERSAL_ENCODING) as file:
        reader = csv.reader(file, quotechar='"', skipinitialspace=True)  # Improved CSV handling
        
        # Skip the header row if it exists
        next(reader, None)  # Skip header
        
        index = 0  # Start index from 0
        # Iterate through the rows in the CSV file
        for row in reader:
            print(f"Processing row: {row}")  # Debugging log to track each row
            
            # Validate the row length
            if len(row) < 3:
                print(f"Skipping row (not enough columns): {row}")
                continue  # Skip rows that don't have at least 3 columns
            
            # Extract questions and answers for Person 1 and Person 2
            person_a_question = row[1].strip() if len(row) > 1 and row[1].strip() else "No question provided"
            person_b_answer = row[2].strip() if len(row) > 2 and row[2].strip() else "No answer provided"
            
            # Create dictionary entry for Person A's question and Person B's answer
            data.append({
                "": f"{index}",
                "question": person_a_question,
                "answer": person_b_answer
            })
            
            index += 1
    
    # Write the data to the JSON file with custom formatting
    with open(json_file, "w", encoding=UNIVERSAL_ENCODING) as d:
        d.write('[')
        for i, item in enumerate(data):
            json.dump(item, d, separators=(',', ':'))
            if i < len(data) - 1:
                d.write(',')
            d.write('\n')
        d.write(']')
    
    print(f"Conversion complete. JSON saved to {json_file}")

# Example Usage
csv_file = 'C:/Users/user/Desktop/AI/Emira/DataCollection/Data/imported/Raw/uncooked/casual_data_windows.csv'  # Replace with your CSV file path
json_file = 'C:/Users/user/Desktop/AI/Emira/DataCollection/Data/imported/Complex6[conversations].json'  # Desired output JSON file path
convert_csv_to_json(csv_file, json_file)




