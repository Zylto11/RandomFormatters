import requests
from bs4 import BeautifulSoup
import json
import random

# --- Death Row Dataset Extraction (Example) ---
def extract_deathrow_qna():
    url = "https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html"
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    inmate_data = []
    
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            inmate_name = cells[0].get_text(strip=True)
            final_words = None
            for cell in cells[1:]:
                text = cell.get_text(strip=True)
                if text.startswith('"') or text.startswith("'"):
                    final_words = text
                    break
            if not final_words and len(cells) >= 2:
                candidate = cells[-1].get_text(strip=True)
                if len(candidate.split()) > 3:
                    final_words = candidate
            if inmate_name and final_words:
                inmate_data.append({
                    "name": inmate_name,
                    "final_words": final_words
                })

    # Create Q&A pairs using playful templates
    question_templates = [
        "Can you give me a final phrase?",
        "What would be your last words if you were on death row?",
        "Give me a final phrase for someone.",
        "Death.",
        "In a playful twist, give me a unique last word.",
        "What interesting message would you leave behind in your final words?",
        "How could you express a cocktail of emotions with some final words?"
    ]
    filler_list = ["Hmm", "Well", "How about", "Ah", "Uhh"]
    
    qna_list = []
    for inmate in inmate_data:
        template = random.choice(question_templates)
        filler = random.choice(filler_list)
        # Format the question – you might include the inmate's name if desired.
        question = f"{filler} {template}"
        answer = inmate["final_words"]
        qna_list.append({
            "question": question,
            "answer": answer
        })
    return qna_list

# --- Hate Speech Dataset Extraction ---
def extract_hate_speech_qna():
    # Placeholder for hate speech dataset extraction logic.
    # For example, if this dataset contains text with labels, you might decide
    # to treat the text as the "answer" and generate a question such as:
    # "What is an example of hate speech content?"
    qna_list = []
    # Example (you would replace this with actual parsing):
    # with open('hate_speech_data.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    # for entry in data:
    #     question = "Can you provide an example of hate speech?"
    #     answer = entry.get('text', '')
    #     qna_list.append({"question": question, "answer": answer})
    return qna_list

# --- Joke Dataset Extraction ---
def extract_joke_dataset_qna():
    # Placeholder for jokes dataset extraction.
    # For a joke, if the structure is something like:
    # { "setup": "...", "punchline": "..." }
    # you might decide to treat the setup as the question and the punchline as the answer.
    qna_list = []
    # Example:
    # with open('jokes.json', 'r', encoding='utf-8') as f:
    #     jokes = json.load(f)
    # for joke in jokes:
    #     qna_list.append({"question": joke.get("setup", "Tell me a joke:"), "answer": joke.get("punchline", "")})
    return qna_list

# --- Reddit Dataset Extraction ---
def extract_reddit_dataset_qna():
    # Placeholder for Reddit dataset extraction.
    # Depending on the dataset structure, you might extract a post's title as the question
    # and the top comment as the answer (or vice versa).
    qna_list = []
    # Example:
    # with open('reddit_dataset.json', 'r', encoding='utf-8') as f:
    #     posts = json.load(f)
    # for post in posts:
    #     question = post.get("title", "Reddit post:")
    #     answer = post.get("selftext", "")
    #     qna_list.append({"question": question, "answer": answer})
    return qna_list

# --- NLP Datasets (GitHub Overview) Extraction ---
def extract_nlp_datasets_qna():
    # Placeholder for extracting Q&A pairs from NLP datasets overview.
    # You might decide to extract entries that already represent Q&A pairs or
    # simply generate questions based on dataset descriptions.
    qna_list = []
    return qna_list

# --- Urban Dictionary Dataset Extraction ---
def extract_urban_dictionary_qna():
    # Placeholder for urban dictionary words dataset.
    # You could, for instance, treat the dictionary entry as a Q&A pair,
    # where the "word" is the question and the "definition" is the answer.
    qna_list = []
    # Example:
    # with open('urban_dictionary.csv', 'r', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         question = f"What does the word '{row.get('word', '')}' mean?"
    #         answer = row.get("definition", "")
    #         qna_list.append({"question": question, "answer": answer})
    return qna_list

# --- Main Aggregation Function ---
def main():
    combined_qna = []
    
    # Extract Q&A pairs from each dataset.
    combined_qna.extend(extract_deathrow_qna())
    combined_qna.extend(extract_hate_speech_qna())
    combined_qna.extend(extract_joke_dataset_qna())
    combined_qna.extend(extract_reddit_dataset_qna())
    combined_qna.extend(extract_nlp_datasets_qna())
    combined_qna.extend(extract_urban_dictionary_qna())
    
    # Optionally, merge your additional 50,000 NLP samples here.
    # For example, if those are already in Q&A format:
    # with open('local_nlp_qna.json', 'r', encoding='utf-8') as f:
    #     local_samples = json.load(f)
    #     combined_qna.extend(local_samples.get('qna', []))
    
    output_data = {"qna": combined_qna}
    
    # Save the combined Q&A JSON to a file.
    output_filename = "combined_qna.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    
    print(f"Combined Q&A data saved to {output_filename}")

if __name__ == "__main__":
    main()
