from serpapi import GoogleSearch

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_google_results(query):
    params = {
        "q": query,
        "num": 50,  # Get 50 results
        "api_key": "4a7c367bf5517d0d113bef4359092091d6766b7f42a4fed6326457835ff2b816"  # You need to get a SerpApi key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    links = [result['link'] for result in results['organic_results']]
    return links




def crawl_website(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the domain
        domain = urlparse(url).netloc
        
        # Extract the title
        title = soup.title.string if soup.title else 'No title'

        # Extract the meta description
        meta = soup.find("meta", attrs={"name": "description"})
        description = meta['content'] if meta else 'No description'
        
        return {"domain": domain, "title": title, "description": description}
    
    except Exception as e:
        return {"domain": url, "title": "Error", "description": str(e)}


def main(query):
    # Get first 50 Google search results
    urls = get_google_results(query)
    
    # Crawl each URL and extract domain, title, description
    results = []
    for url in urls:
        data = crawl_website(url)
        results.append(data)
    
    return results

# Example query
query = "Top 10 IT services and consulting companies in delhi ncr"
results = main(query)
for result in results:
    print(f"Domain: {result['domain']}")
    print(f"Title: {result['title']}")
    print(f"Description: {result['description']}")
    print("-" * 50)
