import json

# Paths
input_file = r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\imported\Raw\uncooked\shittyParquetFile.txt'
output_file = r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\imported\Raw\uncooked\shittyParquetFile.json'

# Read and fix data
with open(input_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines()]

# Fix the data by wrapping it in a list and write to JSON with indenting
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(lines, f, separators=(',', ':'), indent=4)


