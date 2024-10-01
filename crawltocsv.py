from serpapi import GoogleSearch
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv

# Function to get the first 50 Google search results
def get_google_results(query):
    params = {
        "q": query,
        "num": 100,  # Get 50 results
        "location":"New Delhi",
        "api_key": "4a7c367bf5517d0d113bef4359092091d6766b7f42a4fed6326457835ff2b816"  # You need to get a SerpApi key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    links = [result['link'] for result in results['organic_results']]
    return links

# Function to crawl each website and extract domain, title, and description
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

# Function to save the data to a CSV file
def save_to_csv(data, filename='results2.csv'):
    headers = ['Domain', 'Title', 'Description']
    
    # Open the file in write mode
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Write each row of data
        for row in data:
            writer.writerow({'Domain': row['domain'], 'Title': row['title'], 'Description': row['description']})
            print(f"Domain: {row['domain']}")
            print(f"Title: {row['title']}")
            print(f"Description: {row['description']}")
            print("-" * 50)
    
    print(f"Data saved to {filename}")

# Main function that runs the search and crawling process
def main(query):
    # Get first 50 Google search results
    urls = get_google_results(query)
    
    # Crawl each URL and extract domain, title, description
    results = []
    for url in urls:
        data = crawl_website(url)
        results.append(data)
    
    # Save the crawled data to a CSV file
    save_to_csv(results)

# Example usage
query = "Cloud computing solutions"
main(query)

#it consulting companies in delhi ncr
#it consulting firms in delhi ncr
#it solutions delhi ncr
#it consultancy delhi ncr
#it companies delhi ncr
#it services delhi ncr
#msp provider delhi ncr
#msp delhi ncr
#it services gurugram
#it services noida
#it services delhi


#api parameter changed
#msp provider
#it solutions
#why i need it consulting for my business
#it firms near me
#Enterprise IT solutions
#Managed IT services
#