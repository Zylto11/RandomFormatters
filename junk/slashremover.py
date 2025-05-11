import json



#dosent format !!!



# Specify input and output file names
input_file = r"C:\Users\user\Desktop\AI\Emira\punk_hate_speech_cleaned.json"
output_file = r"C:\Users\user\Desktop\AI\Emira\hate_speechClean.json"

# Load the JSON dataset
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Remove literal '\' and '/' from each text field
for entry in data:
    if "text" in entry:
        entry["text"] = entry["text"].replace("\\", "").replace("/", "")

# Dump to a JSON-formatted string
json_str = json.dumps(data, indent=4, ensure_ascii=False)

# Remove all backslashes from the JSON string (this may remove essential escapes)
json_str = json_str.replace("\\", "")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_str)

print(f"Cleaned dataset saved as '{output_file}'.")
