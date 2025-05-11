import yaml
import json

# Function to read the YAML file and convert it to the desired flat JSON format
def convert_yaml_to_json(yml_file, json_file):
    # Open and read the .yml file
    with open(yml_file, 'r') as file:
        yml_data = yaml.safe_load(file)
    if yml_file is not None:
        json_data = []
        for index, entry in enumerate(yml_data):
            # Ensure the entry contains two elements (question and answer)
            if len(entry) >= 2:
                question = entry[0]
                answer = entry[1]
            else:
                question = ""
                answer = ""

            # Append the formatted entry to the JSON data list
            json_data.append({
                "": str(index),  # Index as a string under the empty key
                "question": question,
                "answer": answer
            })

    elif yml_file is None:
        print("yml data not loaded properly.")
        quit()

    # Write the JSON data to the output file in compact format (no spaces/indentation)
    with open(json_file, 'w') as file:
        json.dump(json_data, file, separators=(',', ':'))

convert_yaml_to_json(r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\imported\Raw\Complex3[Raw].yml', r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\imported\Raw\Complex3[conversations].json')
