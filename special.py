import json
import random

def random_symbol():
    # Symbols and their corresponding weights (probabilities)
    symbols = ['?', '!', '~']
    weights = [0.8, 0.11, 0.09]  # 80%, 10%, and 10%

    return random.choices(symbols, weights=weights, k=1)[0]


path =r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\imported\Raw\uncooked\shittyParquetFile.json'
outpath = r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\imported\Raw\uncooked\Complex7[information].json'

with open(path , 'r')as a:
    input_data = json.load(a)
# List to store output data
output_data = []

# Process each item in the input data
for item in input_data:
    # Parse the JSON string into a dictionary
    parsed_item = json.loads(item)
    
    # Extract the question stem and choices
    question_stem = parsed_item["question_stem"]
    choices = parsed_item["choices"]["text"]
    
    # Add a '?' to the question stem
    question_with_question_mark = f"{question_stem}{random_symbol()}"
    
    # Generate a new entry for each choice
    for choice in choices:
        output_data.append({
            "question": question_with_question_mark,
            "answer": f"{question_with_question_mark} {choice}"
        })

# Open the file and write the formatted JSON data
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(json.dumps(output_data, indent=4))
