import json
import datasets
import pandas as pd


#TODO:
from datasets import load_dataset

ds = load_dataset("iamtarun/python_code_instructions_18k_alpaca")

#https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K?row=7


def pleh1():
    
    # Path to the JSON file
    json_file = r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\imported\Raw\uncooked\shittyParquetFile.json'

    # Load the JSON file into a DataFrame
    df = pd.read_json(json_file)

    # Create a function to extract and format the required fields (question and answer)
    def format_data(row):
        question = row['question_stem']  # The question is the question_stem
        answer_label = row['answerKey']  # The answer is based on the answerKey
        choices = row['choices']['text']  # Get the list of choice texts

        # Find the index of the correct choice using the answerKey (e.g., 'A', 'B', 'C', 'D')
        label_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        answer = choices[label_to_index.get(answer_label, 0)]  # Default to 0 if answerKey is not valid

        # Add the question to the front of the answer
        combined_answer = f"{question} {answer}"

        return {
            "question": question,
            "answer": combined_answer
        }

    # Apply the function to format each row
    formatted_data = [format_data(row) for _, row in df.iterrows()]

    # Save the data as JSON
    output_file = r'C:\Users\user\Desktop\AI\Emira\DataCollection\Data\formatted_data_combined.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=4)

    print(f"Formatted data saved to {output_file}")

def combine_and_extract_qna_PARQUET(parquet_file1, parquet_file2, output_json_file):
    # Read both Parquet files into DataFrames
    df1 = pd.read_parquet(parquet_file1)
    df2 = pd.read_parquet(parquet_file2)

    # Combine the two DataFrames (assuming concatenation is needed)
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Initialize a list to hold the extracted Q&A data
    qna_data = []

    # Iterate over each row in the DataFrame
    for _, row in combined_df.iterrows():
        # Convert row to dictionary (assuming row is a dict-like object)
        record = row.to_dict()

        # Create a dictionary to hold this record's Q&A
        record_qna = {
            "id": record.get("id", ""),
            "question": record.get("question", ""),
            "annotations": []
        }

        # Extract the main question and answer (if available)
        nq_answer = record.get("nq_answer", [])
        if record_qna["question"] and nq_answer:
            record_qna["annotations"].append({
                "type": "singleAnswer",
                "question": record_qna["question"],
                "answer": nq_answer
            })

        # Also check and extract any other questions/answers in 'qaPairs'
        qa_pairs = record.get("annotations", {}).get("qaPairs", [])
        for qa_pair in qa_pairs:
            for q, a in zip(qa_pair.get('question', []), qa_pair.get('answer', [])):
                if q and a:
                    record_qna["annotations"].append({
                        "type": "multipleQAs",
                        "question": q,
                        "answer": a
                    })

        # Add the Q&A data for this record to the main list
        qna_data.append(record_qna)

    # Write the list of Q&A data to a JSON file with an indent of 4
    with open(output_json_file, 'w') as json_file:
        json.dump(qna_data, json_file, indent=4)

    print(f"Data extracted and saved to {output_json_file}")

def extract_question_answer(file_path,output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read all lines and parse them as JSON entries
        lines = file.readlines()
        
        for line in lines:

            # Parse each line as a JSON object
            data = json.loads(line.strip())
            
            # Extracting questions and answers
            questions = []
            answers = []
            
            # Check if 'qaPairs' exists in the JSON
            if 'qaPairs' in data['annotations']:
                for qa in data['annotations']['qaPairs']:
                    for q, a in zip(qa['question'], qa['answer']):
                        questions.append(q)
                        answers.append(a)
            
    with open(output_path,'w')as OUTptt:
        pass


