from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from modules import extract_page,get_page
import time
import random

base_url = "https://books.toscrape.com/"
all_records = []
page_number = 1
while True:
    response = get_page(base_url)
    if response is None:
        print(f"Failed to fetch page: {base_url}. Stopping the scraping process.")
        break  # Exit the loop if the page fetch fails
    soup = BeautifulSoup(response.content, 'html.parser')
    records = extract_page(soup)
    print('Number of records extracted from this page:', len(records))
    all_records.extend(records)
    next_page = soup.find('li', class_='next').find('a')['href']
    if next_page is None:
        print('No more pages to scrape.')
        break
    next_page_url = urljoin(base_url, next_page)
    base_url = next_page_url
    page_number += 1
    time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds


print('Number of records extracted:', len(all_records))

with open('data/books.json', 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=4)
with open('data/books.json', 'r', encoding='utf-8') as f:
        loaded_records=json.load(f)
print(all_records==loaded_records)


