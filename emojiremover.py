import json 
import re

# Open and read the file
with open("DataCollection/Data/imported/Raw/uncooked/bad_word_training.txt", "r", encoding="utf-8") as f:
    lines = f.read().strip().split("\n")

# Output list
punk_dataset = []

# Class mapping
label_map = {0: "Hate Speech", 1: "Offensive Language", 2: "Neutral"}

# Regex to detect emojis and file links
emoji_pattern = re.compile(
    "[" 
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Symbols & pictographs
    "\U0001F680-\U0001F6FF"  # Transport & map symbols
    "\U0001F700-\U0001F77F"  # Alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric shapes
    "\U0001F800-\U0001F8FF"  # Supplemental symbols
    "\U0001F900-\U0001F9FF"  # Supplemental pictographs
    "\U0001FA00-\U0001FA6F"  # Symbols and pictographs
    "\U0001FA70-\U0001FAFF"  # More symbols
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"  # Enclosed characters
    "]+", flags=re.UNICODE
)

file_link_pattern = re.compile(r"https?://\S+|www\.\S+|(\.jpg|\.png|\.gif|\.mp4|\.pdf|\.zip|\.exe)", re.IGNORECASE)

# Process each line
for line in lines:
    parts = line.split(",", 6)  # Split into 7 parts; the last part is the tweet
    if len(parts) < 7:
        continue  # Skip malformed lines
    
    # Check if the class field is a valid integer
    if not parts[5].strip().isdigit():
        continue  # Skip header or malformed class values

    tweet = parts[6].strip()
    label = int(parts[5])  # Convert class to int

    # Remove HTML entities
    tweet = tweet.replace("&amp;", "&").replace("&#57361;", "").replace("&#8220;", "").replace("&#8221;", "")

    # Check if the tweet is empty or contains emojis/file links
    if not tweet or emoji_pattern.search(tweet) or file_link_pattern.search(tweet):
        continue  # Skip tweets with emojis or links

    # Append clean entry
    punk_dataset.append({
        "text": tweet,
        "label": label_map.get(label, "Unknown")
    })

# Save as JSON file
output_file = "punk_hate_speech_cleaned.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(punk_dataset, f, indent=4)

print(f"Cleaned dataset saved as '{output_file}'.")
