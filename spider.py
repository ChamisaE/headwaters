import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

def filter_url(url, keyword):
    """
    Check if the keyword is in the URL.
    """
    return keyword in url

def normalize_url(url):
    """
    Normalize the URL by stripping the trailing slash and fragment.
    """
    parsed_url = urlparse(url)
    normalized_path = parsed_url.path.rstrip('/')
    normalized_url = parsed_url._replace(path=normalized_path, fragment='').geturl()
    return normalized_url

def get_page(start_url, keyword, file_handle):
    visited_urls = set()
    queue = [start_url]
    
    while queue:
        url = queue.pop(0)
        normalized_url = normalize_url(url)
        
        if normalized_url in visited_urls:
            continue
        
        print(f"Visiting: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            continue
        
        visited_urls.add(normalized_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')
        
        for tag in a_tags:
            href = tag.get("href")
            if href:
                abs_url = urljoin(url, href)
                if filter_url(abs_url, keyword):
                    normalized_abs_url = normalize_url(abs_url)
                    if normalized_abs_url not in visited_urls:
                        queue.append(abs_url)
                        # Ensure the original URL is written to file, not the normalized one
                        file_handle.write(abs_url + '\n')

# Prompt the user for the URL to scrape    
user_url = input("What URL would you like to scrape? ")

# Prompt the user for a keyword that must exist in the URL 
user_keyword = input("Enter the keyword that must exist in the URL: ")

# Generate a unique file name using the current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"filtered_urls_{timestamp}_end_part.txt"

# Open the file in write mode
with open(file_name, 'w') as file_handle:
    # Call the function 
    get_page(user_url, user_keyword, file_handle)

print(f"Filtered URLs have been written to {file_name}")
