
import requests
import time
import random
retryable_status_codes=[429,500,502,503,504]

def create_session():
    session=requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })
    return session

def get_retry_after(response):
    retry_after=response.headers.get('Retry-After')
    if retry_after:
        try:
            return int(retry_after)
        except ValueError:
            return None
    return None

def exponential_backoff(attempt, base_delay=2):
    delay=base_delay * (2 ** (attempt - 1))
    jitter=random.uniform(0, 1)
    return delay + jitter

def get_page(url,max_retries=3):
    session=create_session()
    for attempt in range(1, max_retries + 1):
        try:
            response=session.get(url,timeout=30)
            # successful response handling
            if response.status_code==200 and response.headers.get('Content-Type','').startswith('text/html') and response.content:
                print(f"Successfully fetched page: {url} on attempt {attempt}")
                return response
            # retryable status code handling
            if response.status_code in retryable_status_codes:
               if attempt==max_retries:
                   print(f"Max retries reached for URL: {url}. Skipping this page.")
                   return None
               delay=get_retry_after(response)
               if delay is None:
                   delay=exponential_backoff(attempt)
               print(f"Received status code {response.status_code}. Retrying after {delay} seconds. Attempt {attempt} of {max_retries}")
               time.sleep(delay)
               continue
            # non-retryable status code handling
            print(f"Received non-retryable status code {response.status_code}. Skipping this page.")
            return None
        except requests.RequestException as e:
            print(f"Error occurred while making the request: {e} Attempt {attempt} of {max_retries}")
            if attempt==max_retries:
                print(f"Max retries reached for URL: {url}. Skipping this page.")
                return None
            time.sleep(exponential_backoff(attempt))  # Wait before retrying
            continue

def extract_books(book):
    record={}
    image_container=book.find('div', class_='image_container').find('img')
    image=image_container.get('src') if image_container else None
    rating_container=book.find('p', class_='star-rating')
    rating=rating_container.get('class') if rating_container else None
    title_container=book.find('h3').find('a')
    title=title_container.get('title') if title_container else None
    #short_title=title_container.get_text(strip=True) if title_container else None
    link=title_container.get('href') if title_container else None
    price_container=book.find('p', class_='price_color')
    price=price_container.get_text(strip=True) if price_container else None
    availability_container=book.find('p', class_='instock availability')
    availability=availability_container.get_text(strip=True) if availability_container else None
    record['image']=image
    record['rating']=rating
    record['title']=title
    record['link']=link 
    record['price']=price
    record['availability']=availability
    return record


def extract_page(soup):
    records=[]
    books=soup.find_all('article', class_='product_pod')
    for book in books:
        book=extract_books(book)
        records.append(book)
    return records









