import json
import re

# Load the dataset
data = r'C:\Users\user\Desktop\CODE\datasetFiltering\DataStorage\processed_jokes_extreme.json'
savepath = r'C:\Users\user\Desktop\CODE\datasetFiltering\DataStorage\processed_jokes_extremeFiltered.json'


with open(data, 'r', encoding='utf-8') as file:
    dataset = json.load(file)

# Function to replace Unicode escape sequences with the actual characters as specified in replacements
def replace_unicode_with_characters(text):
    # Check if text is a string containing raw escape sequences
    if isinstance(text, str):
        # Replace known Unicode sequences with their respective characters
        replacements = {
            r'\u2014':"_", #longer underscore
            r'\u2019': "'", # '
            r'\u00e9': 'e',  # é
            r'\u0142': 't',  # ł
            r'\u0144': 'n',  # ń
            r'\u00f2': 'o',  # ò
            r'\u00e0': 'a',  # à
            r'\u00f3': 'o',  # ó
            r'\u00e7': 'c',  # ç
            r'\u00f9': 'u',  # ù
            r'\u00e7': 'c',  # ç
            r'\u00e6': 'ae',  # æ
            r'\u00f8': 'o',  # ø
            r'\u00fc': 'u',  # ü
            r'\u00e1': 'a',  # á
            r'\u00ed': 'i',  # í
            r'\u00f1': 'n',  # ñ
            r'!':' ', #remove !
            r'@':' ',
            r'#':' ',
            r'^':' ',
            r'`':' ',
            r'\\':' '
            # Add more replacements as needed
        }
        
        # Replace each known escape sequence in the text (make sure it's a string)
        for unicode_seq, char in replacements.items():
            text = text.replace(unicode_seq, char)

    return text

# Modify the dataset
for entry in dataset:
    # Handle 'question' field (can be a string)
    entry['question'] = replace_unicode_with_characters(entry['question'])
    
    # Handle 'answer' field (if it's a list, convert it to a string)
    if isinstance(entry['answer'], list):
        if entry['answer']:  # Check if the list is not empty
            entry['answer'] = replace_unicode_with_characters(entry['answer'][0])  # Use the first item as a string
        else:
            entry['answer'] = "I dont know. Im just an AI afterall."
    else:
        entry['answer'] = replace_unicode_with_characters(entry['answer'])  # If it's a string, just apply directly

# Save the modified dataset to the specified path without escaping non-ASCII characters
with open(savepath, 'w', encoding='utf-8') as ads:
    json.dump(dataset, ads, indent=4, ensure_ascii=False)

print("Dataset successfully modified and saved.")