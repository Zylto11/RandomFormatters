import requests
from bs4 import BeautifulSoup
import time
import urllib3
from urllib.parse import urljoin

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_inmate_links():
    base_url = r'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
    response = requests.get(base_url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    inmate_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "dr_info" in href and href.endswith("last.html"):
            full_url = urljoin(r"https://www.tdcj.texas.gov/", href)
            inmate_links.append(full_url)
    
    return inmate_links

def get_last_words(url):
    print(f"Fetching last words from: {url}")
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    last_words_section = soup.find("p", text=lambda x: x and "Last Statement" in x)
    if last_words_section:
        last_words = last_words_section.find_next_sibling("p").get_text(strip=True)
        return last_words
    else:
        return "Last Statement not found."

def main():
    inmate_links = get_inmate_links()
    
    with open("tdcj_last_words.txt", "w", encoding="utf-8") as file:
        print("Created file at destination.")
        for index, link in enumerate(inmate_links):
            print(f"Processing inmate {index + 1}:")
            last_words = get_last_words(link)
            print(f"Last Words: {last_words}")
            file.write(f"Inmate {index + 1} Last Words:\n{last_words}\n\n")
            time.sleep(1)  # Prevents overwhelming the server
    
    print("Scraping complete. Last words saved in tdcj_last_words.txt")

if __name__ == "__main__":
    main()
